-- tables
CREATE TABLE IF NOT EXISTS rc.documents (doc_id STRING, case_id STRING, doc_type STRING, version INT64, source_uri STRING, page_count INT64, uploaded_by STRING, uploaded_ts TIMESTAMP, sha256 STRING);
CREATE TABLE IF NOT EXISTS rc.document_chunks (chunk_id STRING, doc_id STRING, page_start INT64, page_end INT64, text STRING, tokens INT64, sec_path STRING);
CREATE TABLE IF NOT EXISTS rc.embeddings (chunk_id STRING, doc_id STRING, emb VECTOR<FLOAT64>, created_ts TIMESTAMP);
CREATE TABLE IF NOT EXISTS rc.intervenor_requests (rq_id STRING, case_id STRING, requester STRING, question STRING, due_date DATE, status STRING);
CREATE TABLE IF NOT EXISTS rc.answers (ans_id STRING, rq_id STRING, draft STRING, final STRING, state STRING, created_ts TIMESTAMP, updated_ts TIMESTAMP);
CREATE TABLE IF NOT EXISTS rc.citations (ans_id STRING, chunk_id STRING, doc_id STRING, page_from INT64, page_to INT64, quote STRING, confidence FLOAT64);
