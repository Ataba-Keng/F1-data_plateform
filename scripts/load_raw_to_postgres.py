import json
import logging
import os
import boto3
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
S3_RAW_BUCKET = os.getenv("S3_RAW_BUCKET", "f1-data-platform-raw-dev")

DB_USER = os.getenv("DBT_RDS_USER", "f1_admin")
DB_PASS = os.getenv("DBT_RDS_PASSWORD", "keng96837671")
DB_HOST = os.getenv("DBT_RDS_HOST", "172.17.0.1")
DB_PORT = os.getenv("DBT_RDS_PORT", "5432")
DB_NAME = os.getenv("DBT_RDS_DB", "f1_db")

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)
s3_client = boto3.client("s3", region_name=AWS_REGION,endpoint_url=AWS_ENDPOINT_URL)

# Les 3 entités réellement extraites depuis OpenF1
ENTITIES = ["meetings", "sessions", "drivers"]


def setup_raw_schema():
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        for entity in ENTITIES:
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS raw.{entity} (
                    payload JSONB,
                    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
    logging.info("Schéma raw et tables initialisés.")


def load_s3_to_postgres(table_name: str, s3_key: str):
    logging.info(f"Téléchargement de s3://{S3_RAW_BUCKET}/{s3_key}...")
    try:
        response = s3_client.get_object(Bucket=S3_RAW_BUCKET, Key=s3_key)
        records = json.loads(response["Body"].read().decode("utf-8"))
    except Exception as e:
        logging.error(f"Erreur lors de la lecture S3 ({s3_key}): {e}")
        return

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE raw.{table_name};"))
        insert_query = text(f"INSERT INTO raw.{table_name} (payload) VALUES (:payload)")
        for record in records:
            conn.execute(insert_query, {"payload": json.dumps(record)})

    logging.info(f"Table raw.{table_name} chargée avec {len(records)} lignes.")


def run_loader(year: int = 2024):
    setup_raw_schema()
    for entity in ENTITIES:
        s3_key = f"seasons/year={year}/{entity}.json"
        load_s3_to_postgres(entity, s3_key)


if __name__ == "__main__":
    run_loader(2024)