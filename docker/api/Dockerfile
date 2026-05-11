# =============================================================================
#  docker/api/Dockerfile — Image FastAPI pour l'inférence Rakuten
# -----------------------------------------------------------------------------
#  Build context attendu : racine du projet (".").
#  Build :
#    docker compose build api
#  ou :
#    docker build -f docker/api/Dockerfile -t api-rakuten .
# =============================================================================

FROM python:3.11-slim

# Pas de .pyc, sortie stdout/stderr non bufférisée (logs en direct)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# --- Dépendances système minimales ------------------------------------------
#  curl utile pour HEALTHCHECK + debug réseau (ex: ping MLflow).
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# --- Dépendances Python -----------------------------------------------------
COPY docker/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# --- Code applicatif --------------------------------------------------------
#  On copie uniquement ce dont l'API a besoin à l'exécution :
#    - src/api, src/services, src/utils  → logique applicative
#    - data/processed/Y_train_encode.csv → mapping métier (code → libellé)
#  Pas de data/raw (volumineux) ni de notebooks.
COPY src/__init__.py        /app/src/__init__.py
COPY src/api/               /app/src/api/
COPY src/services/          /app/src/services/
COPY src/utils/             /app/src/utils/
# src/features/ est nécessaire au moment de l'unpickle du modèle :
# le pipeline scikit-learn entraîné contient des références vers
# src.features.text_features (utilisé dans les FunctionTransformer).
# Sans ce dossier l'API plante au chargement avec :
#   ModuleNotFoundError: No module named 'src.features'
COPY src/features/          /app/src/features/
COPY data/processed/Y_train_encode.csv /app/data/processed/Y_train_encode.csv

# --- Port exposé ------------------------------------------------------------
EXPOSE 8000

# --- Healthcheck ------------------------------------------------------------
#  Endpoint racine "/" renvoie {"message": "API Rakuten opérationnelle"}.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -fs http://localhost:8000/ || exit 1

# --- Démarrage --------------------------------------------------------------
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
