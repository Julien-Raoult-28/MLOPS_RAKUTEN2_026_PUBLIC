"""
Service de prédiction pour l'API Rakuten.

Ce module charge un modèle MLflow (via run_id ou via le Model Registry)
et exécute une prédiction sur un produit décrit par :

- designation : titre du produit
- description : description textuelle

Le service est compatible avec :
- MLflow FileStore (runs:/)
- MLflow Model Registry (models:/)
- MLflow pyfunc (modèles génériques)

Le backend MLflow utilisé est SQLite (mlflow.db), ce qui permet
l'utilisation du Model Registry et du mode hybride dans l'API.
"""

import time
from datetime import datetime
import pandas as pd
import mlflow


# ------------------------------------------------------------
# Configuration MLflow (OBLIGATOIRE pour le mode hybride)
# ------------------------------------------------------------
mlflow.set_tracking_uri("sqlite:///mlflow.db")


def load_model(run_id: str | None):
    """
    Charge un modèle MLflow.

    Paramètres
    ----------
    run_id : str | None
        - Si fourni : charge le modèle associé au run (runs:/)
        - Si None : charge le modèle en Production dans le Model Registry

    Retour
    ------
    mlflow.pyfunc.PyFuncModel
        Modèle MLflow prêt à exécuter une prédiction.
    """

    if run_id:
        model_uri = f"runs:/{run_id}/model"
    else:
        model_uri = "models:/rakuten_classifier/Production"

    return mlflow.pyfunc.load_model(model_uri)


def predict_product(designation: str, description: str, run_id: str | None):
    """
    Effectue une prédiction via un modèle MLflow (pyfunc).

    Paramètres
    ----------
    designation : str
        Titre du produit.
    description : str
        Description textuelle du produit.
    run_id : str | None
        Identifiant MLflow pour charger un modèle spécifique.
        Si None, charge le modèle en Production.

    Retour
    ------
    dict
        Résultat structuré contenant :
        - les données d'entrée
        - le code de prédiction
        - le label métier
        - le temps d'inférence
        - les métadonnées MLflow
    """

    try:
        # Charger le modèle MLflow
        model = load_model(run_id)

        # Préparer les données pour pyfunc
        df = pd.DataFrame([{
            "designation": designation,
            "description": description
        }])

        # Exécuter la prédiction
        start = time.time()
        pred = model.predict(df)
        end = time.time()

        # Le modèle sklearn renvoie un array numpy
        prediction_code = int(pred[0])
        label = str(prediction_code)  # mapping métier simplifié

        return {
            "designation": designation,
            "description": description,
            "prediction": {
                "prediction_code": prediction_code,
                "label": label,
                "confidence": None,  # LinearSVC ne fournit pas de probas
                "inference_time_ms": round((end - start) * 1000, 3),
                "model_uuid": "unknown",
                "model_version": "1",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
            "run_id": run_id,
        }

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la prédiction : {e}")
