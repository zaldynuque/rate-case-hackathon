import os
from fastapi import FastAPI
from google.cloud import bigquery
import vertexai
from vertexai.preview.language_models import TextEmbeddingInput, TextEmbeddingModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET", "rc")
LOCATION = os.getenv("LOCATION", "us-central1")
MODEL = os.getenv("EMBED_MODEL", "text-embedding-004")

app = FastAPI()
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = TextEmbeddingModel.from_pretrained(MODEL)
bq = bigquery.Client()

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

@app.post("/embed_missing")
def embed_missing(limit: int = 200):
    sql = f"""WITH missing AS (
      SELECT chunk_id, doc_id, text FROM `{PROJECT_ID}.{BQ_DATASET}.document_chunks`
      WHERE chunk_id NOT IN (SELECT chunk_id FROM `{PROJECT_ID}.{BQ_DATASET}.embeddings`)
    ) SELECT * FROM missing LIMIT {limit}"""
    rows = list(bq.query(sql).result())
    if not rows:
        return {"embedded": 0}
    texts = [r[2] for r in rows]
    emb_outputs = model.get_embeddings([TextEmbeddingInput(text=t) for t in texts])
    for r, e in zip(rows, emb_outputs):
        emb_array = ",".join([str(v) for v in e.values])
        bq.query(f"""INSERT `{PROJECT_ID}.{BQ_DATASET}.embeddings` (chunk_id, doc_id, emb, created_ts)
        VALUES ('{r[0]}','{r[1]}', VECTOR<FLOAT64>[{emb_array}], CURRENT_TIMESTAMP())""").result()
    return {"embedded": len(rows)}
