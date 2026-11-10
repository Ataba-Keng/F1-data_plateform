FROM apache/airflow:2.9.1-python3.11

USER airflow

# Installation des dépendances Python requises par les scripts et les tâches Airflow
RUN pip install --no-cache-dir \
    dbt-postgres==1.8.2 \
    boto3 \
    requests \
    psycopg2-binary \
    sqlalchemy