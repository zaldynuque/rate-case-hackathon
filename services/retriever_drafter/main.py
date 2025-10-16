import os
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview.language_models import TextEmbeddingModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET", "rc")
LOCATION = os.getenv("LOCATION", "us-central1")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-004")
GEN_MODEL = os.getenv("GEN_MODEL", "gemini-1.5-pro")

vertexai.init(project=PROJECT_ID, location=LOCATION)
emb_model = TextEmbeddingModel.from_pretrained(EMBED_MODEL)
llm = GenerativeModel(GEN_MODEL)
bq = bigquery.Client()
app = FastAPI()

class Ask(BaseModel):
    case_id: str = "CASE-001"
    question: str
    k: int = 8

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

@app.post("/ask")
def ask(payload: Ask):
    q_emb = emb_model.get_embeddings([payload.question])[0].values
    emb_array = ",".join([str(v) for v in q_emb])
    sql = f"""SELECT c.chunk_id, c.doc_id, c.text, VECTOR_DISTANCE(e.emb, VECTOR<FLOAT64>[{emb_array}]) AS score
    FROM `{PROJECT_ID}.{BQ_DATASET}.embeddings` e
    JOIN `{PROJECT_ID}.{BQ_DATASET}.document_chunks` c USING (chunk_id, doc_id)
    JOIN `{PROJECT_ID}.{BQ_DATASET}.documents` d USING (doc_id)
    WHERE d.case_id = @case_id
    ORDER BY score
    LIMIT @k"""
    job = bq.query(sql, job_config=bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("case_id", "STRING", payload.case_id),
        bigquery.ScalarQueryParameter("k", "INT64", payload.k)
    ]))
    rows = list(job.result())
    context = "\n\n".join([f"[doc {r[1]} | chunk {r[0]}]\n{r[2]}" for r in rows])
    system = ("You are a rate case answer assistant. Answer concisely in the utility's voice. "
              "Cite sources by including the doc_id and short quotes from the context. "
              "If unsure, state what is needed to answer.")
    prompt = f"""{system}
Question: {payload.question}

Context:
{context}

Return JSON with fields 'answer' and 'citations':[{{doc_id,chunk_id,quote}}]."""
    resp = llm.generate_content([Part.from_text(prompt)])
    return {"answer": resp.text}
