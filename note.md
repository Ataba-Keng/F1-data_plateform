marts_bucket_name = "f1-data-platform-marts-dev"
raw_bucket_name = "f1-data-platform-raw-dev"
rds_endpoint = "172.17.0.2"
staging_bucket_name = "f1-data-platform-staging-dev"

DB_USER = os.getenv("DBT_RDS_USER", "f1_admin")
DB_PASS = os.getenv("DBT_RDS_PASSWORD", "keng96837671")
DB_HOST = os.getenv("DBT_RDS_HOST", "172.17.0.1")
DB_PORT = os.getenv("DBT_RDS_PORT", "5432")
DB_NAME = os.getenv("DBT_RDS_DB", "f1_db")