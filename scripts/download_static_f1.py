import io
import logging
import os
import zipfile
import boto3
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

S3_RAW_BUCKET = os.getenv("S3_RAW_BUCKET", "f1-data-platform-raw-dev")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
s3_client = boto3.client("s3", region_name=AWS_REGION)

# Miroir brut des fichiers de données F1
DATA_URL = "https://raw.githubusercontent.com/toUpperCase78/formula1-datasets/master/Formula1_Dataset.zip"


def download_and_upload_raw():
    logging.info("Téléchargement du dataset F1 consolidé...")
    res = requests.get(
        "https://github.com/toUpperCase78/formula1-datasets/raw/master/Formula1_Dataset.zip",
        timeout=60,
    )
    res.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        for filename in z.namelist():
            if filename.endswith(".csv"):
                content = z.read(filename)
                s3_key = f"seasons/csv/{os.path.basename(filename)}"
                s3_client.put_object(
                    Bucket=S3_RAW_BUCKET,
                    Key=s3_key,
                    Body=content,
                    ContentType="text/csv",
                )
                logging.info(f"Fichier brut chargé : s3://{S3_RAW_BUCKET}/{s3_key}")


if __name__ == "__main__":
    download_and_upload_raw()