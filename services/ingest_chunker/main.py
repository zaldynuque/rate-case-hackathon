import os, hashlib, uuid
from fastapi import FastAPI, UploadFile, File
from google.cloud import documentai_v1 as docai, bigquery

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET", "rc")
LOCATION = os.getenv("LOCATION", "us")
PROCESSOR_ID = os.getenv("DOCAI_PROCESSOR_ID")

app = FastAPI()
bq = bigquery.Client()

def chunk_text(txt: str, max_tokens=900, overlap=150):
    words = txt.split()
    step = max_tokens - overlap
    for i in range(0, len(words), step):
        yield " ".join(words[i:i+max_tokens])

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), case_id: str = "CASE-001", doc_type: str = "EXHIBIT"):
    content = await file.read()
    sha = hashlib.sha256(content).hexdigest()

    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
    client = docai.DocumentProcessorServiceClient()
    req = docai.ProcessRequest(name=name, raw_document=docai.RawDocument(content=content, mime_type=file.content_type or "application/pdf"))
    result = client.process_document(request=req)
    text = result.document.text or ""

    doc_id = str(uuid.uuid4())
    bq.query(f"""INSERT `{PROJECT_ID}.{BQ_DATASET}.documents` (doc_id, case_id, doc_type, version, source_uri, page_count, uploaded_by, uploaded_ts, sha256)
    VALUES ('{doc_id}', '{case_id}', '{doc_type}', 1, '', {len(result.document.pages)}, 'hackathon', CURRENT_TIMESTAMP(), '{sha}')""").result()

    rows = []
    for ch in chunk_text(text):
        rows.append({"chunk_id":str(uuid.uuid4()),"doc_id":doc_id,"page_start":1,"page_end":1,"text":ch,"tokens":len(ch.split()),"sec_path":""})
    if rows:
        table = bq.dataset(BQ_DATASET).table("document_chunks")
        bq.insert_rows_json(table, rows)
    return {"doc_id": doc_id, "chunks": len(rows)}
