import mlflow
import pandas as pd
import numpy as np
import time
from datetime import datetime
from pathlib import Path

# ============================================================
# CHARGEMENT DU MAPPING prdtypecode_encoded -> libellé métier
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
MAPPING_PATH = BASE_DIR / "data" / "processed" / "Y_train_encode.csv"

mapping_df = pd.read_csv(MAPPING_PATH)[["prdtypecode_encoded", "libelle_type_code"]].drop_duplicates()
LABEL_MAP = dict(zip(mapping_df["prdtypecode_encoded"], mapping_df["libelle_type_code"]))

print(f">>> Mapping label chargé : {len(LABEL_MAP)} catégories")


# ============================================================
# CHARGEMENT DU MODÈLE MLflow
# ============================================================

def load_model_from_mlflow(run_id: str):
    """
    Charge un modèle MLflow à partir d'un run_id.
    """
    model_uri = f"runs:/{run_id}/model"
    print(f">>> Chargement du modèle depuis : {model_uri}")

    try:
        model = mlflow.sklearn.load_model(model_uri)
        print(">>> Modèle MLflow chargé avec succès")
        return model
    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du modèle MLflow : {e}")


# ============================================================
# PRÉPARATION DES DONNÉES
# ============================================================

def prepare_input(designation: str, description: str) -> pd.DataFrame:
    """
    Prépare les données d'entrée pour le modèle.
    """
    if not designation or not description:
        raise ValueError("Les champs 'designation' et 'description' sont obligatoires.")

    df = pd.DataFrame([{
        "designation": designation,
        "description": description
    }])

    print(">>> Données préparées :", df)
    return df


# ============================================================
# PRÉDICTION + MAPPING + PROBA + TEMPS + METADATA
# ============================================================

def predict_label(model, X: pd.DataFrame):
    """
    Applique le modèle pour prédire la classe et renvoie :
    - le code prédictif (int)
    - le libellé métier
    - la confiance (probabilité)
    - le temps d’inférence
    - les métadonnées du modèle
    """

    try:
        start = time.time()

        # --- Prédiction brute ---
        prediction = model.predict(X)
        pred_value = int(prediction[0])   # numpy.int64 → int Python

        # --- Probabilités si disponibles ---
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            confidence = float(np.max(proba))
        else:
            confidence = None

        # --- Temps d’inférence ---
        inference_time = round((time.time() - start) * 1000, 3)

        # --- Libellé métier ---
        label = LABEL_MAP.get(pred_value, "inconnu")

        # --- Métadonnées MLflow ---
        model_uuid = getattr(model, "metadata", {}).get("model_uuid", "unknown")
        model_version = getattr(model, "metadata", {}).get("model_version", "unknown")

        print(">>> Prédiction brute :", prediction)
        print(">>> Prédiction convertie :", pred_value)
        print(">>> Libellé prédictif :", label)
        print(">>> Confiance :", confidence)
        print(">>> Temps d’inférence (ms) :", inference_time)

        return {
            "prediction_code": pred_value,
            "label": label,
            "confidence": confidence,
            "inference_time_ms": inference_time,
            "model_uuid": model_uuid,
            "model_version": model_version,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la prédiction : {e}")