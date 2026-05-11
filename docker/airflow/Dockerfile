# =============================================================================
#  docker/airflow/Dockerfile — Image Airflow + DAGs Rakuten MLOps
# -----------------------------------------------------------------------------
#  Build context attendu : racine du projet (".").
#  Build :
#    docker build -f docker/airflow/Dockerfile -t airflow-rakuten .
#  ou via docker-compose :
#    docker compose build airflow
# =============================================================================

FROM apache/airflow:2.8.4-python3.11

USER airflow

# --- Dépendances Python spécifiques aux DAGs ---------------------------------
COPY docker/airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# --- Code et données du projet -----------------------------------------------
#  Note : data/ et models/ sont copiés pour permettre un run "out-of-the-box".
#  En production on monterait ces dossiers via des volumes (cf. docker-compose).
COPY dags/   /opt/airflow/dags/
COPY src/    /opt/airflow/src/
COPY data/   /opt/airflow/data/
COPY models/ /opt/airflow/models/

# --- Configuration Airflow ----------------------------------------------------
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=False
ENV AIRFLOW__CORE__EXECUTOR=SequentialExecutor
