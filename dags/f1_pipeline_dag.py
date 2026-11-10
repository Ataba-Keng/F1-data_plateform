from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="f1_medallion_pipeline",
    default_args=default_args,
    description="Pipeline ELT F1 : Ingestion S3, chargement Postgres et transformations dbt",
    schedule_interval="@weekly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["f1", "dbt", "s3", "elt"],
) as dag:

    # Tâche 1 : Ingestion de l'API OpenF1 vers le bucket S3 Raw
    extract_api_to_s3 = BashOperator(
        task_id="extract_api_to_s3",
        bash_command="python /opt/airflow/scripts/extract_raw.py 2024",
    )

    # Tâche 2 : Chargement des fichiers S3 Raw vers le schéma PostgreSQL raw
    load_s3_to_postgres = BashOperator(
        task_id="load_s3_to_postgres",
        bash_command="python /opt/airflow/scripts/load_raw_to_postgres.py 2024",
    )

    # Tâche 3 : Exécution des modèles dbt (Staging et Marts)
    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command="export DBT_ALLOW_EXPERIMENTAL_ADAPTERS=true && cd /opt/airflow/dbt_f1 && dbt run --profiles-dir .",    )

    # Tâche 4 : Exécution des tests dbt pour garantir la qualité de données
    test_dbt_models = BashOperator(
        task_id="test_dbt_models",
        bash_command="export DBT_ALLOW_EXPERIMENTAL_ADAPTERS=true && cd /opt/airflow/dbt_f1 && dbt test --profiles-dir .",
    )

    # Définition des dépendances du pipeline
    extract_api_to_s3 >> load_s3_to_postgres >> run_dbt_models >> test_dbt_models