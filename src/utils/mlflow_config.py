"""
Configuration partagée pour MLflow.

Centralise la lecture du tracking URI afin qu'aucun fichier source ne
contienne d'URL MLflow en dur. Tous les entrypoints (CLI, train, evaluate,
API, scripts) doivent passer par get_tracking_uri().
"""

import os

from dotenv import load_dotenv

# Charge .env une seule fois, à l'import du module.
# Tous les modules qui font `from src.utils.mlflow_config import ...`
# bénéficient automatiquement des variables définies dans .env.
load_dotenv()


def get_tracking_uri() -> str:
    """
    Retourne l'URI du serveur MLflow lue depuis l'environnement.

    Source :
      - en local           → variable MLFLOW_TRACKING_URI du fichier .env
                             (ex: http://localhost:8081)
      - dans un conteneur  → variable MLFLOW_TRACKING_URI injectée par
                             docker-compose.yml (ex: http://mlflow:8080)

    Fallback :
      http://localhost:8081 — port hôte par défaut du conteneur MLflow,
      tel que défini dans .env.example et docker-compose.yml.
    """
    return os.getenv("MLFLOW_TRACKING_URI", "http://localhost:8081")
