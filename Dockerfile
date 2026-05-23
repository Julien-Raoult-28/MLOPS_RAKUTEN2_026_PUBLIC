FROM python:3.11-slim

WORKDIR /mlflow

RUN pip install --no-cache-dir mlflow==3.11.1

EXPOSE 8080

CMD ["mlflow", "server",
"--host", "0.0.0.0",
"--port", "8080",
"--backend-store-uri", "sqlite:////mlflow/data/mlflow.db",
"--artifacts-destination", "/mlflow/data/mlruns",
"--serve-artifacts",
"--allowed-hosts", "*"]
