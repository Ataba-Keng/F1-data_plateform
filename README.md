 # 🏎️ Formula 1 Medallion Data Platform

Pipeline de données automatisé de bout en bout (ELT) pour l'ingestion, le stockage, la transformation et l'orchestration des données de Formule 1 (OpenF1 API).

## 🏗️ Architecture

- **Extraction & Ingestion** : Python (`requests`, `boto3`) pour l'extraction via l'API OpenF1 vers un bucket de stockage brut S3 (**Bronze / Raw layer**).
- **Stockage & Entreposage** : PostgreSQL hébergé sur Docker (**Silver / Staging & Gold / Marts layers**).
- **Transformation & Qualité** : `dbt-postgres` pour le nettoyage, la modélisation dimensionnelle (Star Schema) et les tests de données.
- **Orchestration** : Apache Airflow (Docker Compose) pour l'exécution planifiée et le monitoring des dépendances.

## 🚀 Démarrage Rapide

### 1. Prérequis
- Docker et Docker Compose
- Python 3.10+

### 2. Configuration
```bash
git clone [https://github.com/](https://github.com/)<votre-utilisateur>/f1-data-platform.git
cd f1-data-platform
cp .env.example .env
# Renseignez vos identifiants dans le fichier .env