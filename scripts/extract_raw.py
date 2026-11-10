import json
import logging
import os
import sys
import boto3
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_URL = "https://api.openf1.org/v1"
S3_RAW_BUCKET = os.getenv("S3_RAW_BUCKET", "f1-data-platform-raw-dev")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")

s3_client = boto3.client("s3", region_name=AWS_REGION, endpoint_url=AWS_ENDPOINT_URL)


def fetch_openf1(endpoint: str, params: dict = None) -> list:
    url = f"{BASE_URL}/{endpoint}"
    logging.info(f"Appel API OpenF1 : {url} avec {params}")
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur API ({endpoint}): {e}")
        return []


def upload_to_s3(data: list, bucket: str, key: str) -> None:
    try:
        body = json.dumps(data, indent=2, ensure_ascii=False)
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json"
        )
        logging.info(f"Fichier téléversé : s3://{bucket}/{key}")
    except Exception as e:
        logging.error(f"Erreur S3 ({key}): {e}")
        raise


def run_extraction(year: int):
    logging.info(f"Démarrage de l'extraction OpenF1 pour {year}")

    # 1. Meetings (Grands Prix)
    meetings = fetch_openf1("meetings", {"year": year})
    if meetings:
        upload_to_s3(meetings, S3_RAW_BUCKET, f"seasons/year={year}/meetings.json")

    # 2. Sessions (Essais, Qualifs, Course)
    sessions = fetch_openf1("sessions", {"year": year})
    if sessions:
        upload_to_s3(sessions, S3_RAW_BUCKET, f"seasons/year={year}/sessions.json")

    # 3. Drivers (Extraction via les sessions de type 'Race' pour dédoubler tous les pilotes de la saison)
    if sessions:
        race_sessions = [s["session_key"] for s in sessions if s.get("session_type") == "Race"]
        unique_drivers = {}

        logging.info(f"Récupération des pilotes à travers {len(race_sessions)} courses...")
        for s_key in race_sessions:
            drivers = fetch_openf1("drivers", {"session_key": s_key})
            for d in drivers:
                driver_num = d.get("driver_number")
                if driver_num and driver_num not in unique_drivers:
                    unique_drivers[driver_num] = d

        drivers_list = list(unique_drivers.values())
        logging.info(f"Total pilotes uniques recensés pour {year} : {len(drivers_list)}")
        
        if drivers_list:
            upload_to_s3(drivers_list, S3_RAW_BUCKET, f"seasons/year={year}/drivers.json")


if __name__ == "__main__":
    target_year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    run_extraction(target_year)