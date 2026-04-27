FROM python:3.11-slim

WORKDIR /mlflow

# Installer MLflow (et le driver SQLite est déjà inclus dans Python)
RUN pip install --no-cache-dir mlflow==3.11.1

#Port exposé par le serveur MLflow
EXPOSE 8080

# Commande lancée au démarrage du conteneur
CMD ["mlflow", "server", \
    "--host", "0.0.0.0", \
    "--port", "8080", \
    "--backend-store-uri", "sqlite:////mlflow/data/mlflow.db", \
    "--default-artifact-root", "/mlflow/data/mlruns", \
    "--serve-artifacts"]