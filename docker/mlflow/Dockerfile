FROM python:3.11-slim

WORKDIR /mlflow

# Installer MLflow (et le driver SQLite est déjà inclus dans Python)
RUN pip install --no-cache-dir mlflow==3.11.1

#Port exposé par le serveur MLflow
EXPOSE 8080

# Commande lancée au démarrage du conteneur
#
# --allowed-hosts : MLflow 3.x bloque par défaut les requêtes dont le Host
#   header n'est ni "localhost" ni une IP privée (protection anti DNS rebinding).
#   On autorise explicitement :
#     - "mlflow"      : nom de service Docker (utilisé par Airflow et l'API
#                       depuis le réseau interne `mlops-net`)
#     - "localhost"   : appels depuis la machine hôte via http://localhost:8081
# --artifacts-destination (vs --default-artifact-root) : essentiel pour que
#   les clients (Airflow, API) reçoivent une URI artefact de type
#   "mlflow-artifacts:/..." et passent par le serveur en HTTP, plutôt que
#   d'essayer d'écrire directement dans un chemin local (qui n'existe pas
#   de leur côté → PermissionError).
CMD ["mlflow", "server", \
    "--host", "0.0.0.0", \
    "--port", "8080", \
    "--allowed-hosts", "mlflow:*,localhost:*,localhost", \
    "--backend-store-uri", "sqlite:////mlflow/data/mlflow.db", \
    "--artifacts-destination", "/mlflow/data/mlruns", \
    "--serve-artifacts"]