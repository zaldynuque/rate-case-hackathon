# Rate Case Hackathon Repo
See service code and Terraform. Configure DOCAI_PROCESSOR_ID and GCP credentials.

This is a minimal, runnable starter you can use. It provisions a BigQuery dataset and tables, deploys three Cloud Run services (ingest/chunk, embed, retrieve+draft), and wires a simple Vertex AI flow. A tiny Next.js UI lets reviewers ask questions and see sources.

Languages: Terraform, Python (FastAPI), TypeScript (Next.js).
Services: BigQuery, Cloud Run, Artifact Registry, Workflows (optional), Vertex AI, Document AI, Cloud Storage, Pub/Sub.
Envs: one shared hack env (simplify for hackathon).

# Repo Structure

rate-case-hackathon/
├─ infra/terraform/
│ ├─ main.tf
│ ├─ variables.tf
│ ├─ outputs.tf
│ ├─ iam.tf
│ ├─ bigquery.tf
│ ├─ artifact_registry.tf
│ ├─ cloud_run.tf
│ └─ providers.tf
├─ bigquery/
│ └─ schema.sql
├─ services/
│ ├─ ingest_chunker/ # GCS file → DocAI → chunks → BigQuery
│ │ ├─ main.py
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
│ ├─ embedder/ # chunks → embeddings (Vertex) → BigQuery
│ │ ├─ main.py
│ │ ├─ requirements.txt
│ │ └─ Dockerfile
│ └─ retriever_drafter/ # question → retrieve (BQ ANN) → draft (Vertex)
│ ├─ main.py
│ ├─ requirements.txt
│ └─ Dockerfile
├─ ui/nextjs/
│ ├─ package.json
│ ├─ next.config.js
│ ├─ pages/index.tsx
│ └─ pages/api/proxy.ts
├─ workflows/
│ └─ huddle.yaml # optional orchestration
├─ prompts/
│ └─ draft_prompt.json
├─ scripts/
│ ├─ deploy.sh
│ └─ seed.sh
└─ .env.sample
