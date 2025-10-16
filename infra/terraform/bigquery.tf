resource "google_bigquery_dataset" "rc" { dataset_id=var.dataset_id location=var.location delete_contents_on_destroy=true }
resource "google_bigquery_job" "create_tables" { job_id="rc-schema-ddl" location=var.location query { query=file("${path.module}/../..//bigquery/schema.sql") use_legacy_sql=false } depends_on=[google_bigquery_dataset.rc] }
