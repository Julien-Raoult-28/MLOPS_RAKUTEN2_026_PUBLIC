"""
Service de prédiction pour l’API Rakuten.

Ce module orchestre :
- le chargement du modèle MLflow (run_id ou Model Registry),
- la préparation des données,
- l’exécution de la prédiction,
- le décodage métier,
- la construction d’une réponse structurée.

Il constitue la couche “métier” de l’API FastAPI.
"""

import time
from datetime import datetime
from pathlib import Path
import pandas as pd

from src.api.utils import load_model_from_registry, load_model_from_run


# ---------------------------------------------------------------------------
# Chargement du mapping métier (code → libellé)
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
MAPPING_PATH = BASE_DIR / "data" / "processed" / "Y_train_encode.csv"

MAPPING_DF = pd.read_csv(MAPPING_PATH)[
    ["prdtypecode_encoded", "libelle_type_code"]
].drop_duplicates()

LABEL_MAPPING = dict(
    zip(
        MAPPING_DF["prdtypecode_encoded"].astype(int),
        MAPPING_DF["libelle_type_code"].astype(str),
    )
)


# ---------------------------------------------------------------------------
# Fonction principale de prédiction
# ---------------------------------------------------------------------------

def predict_product(designation: str, description: str, run_id: str | None) -> dict:
    """
    Exécute une prédiction via un modèle MLflow (pyfunc).

    Retourne un dictionnaire complet contenant :
    - prediction_code
    - label
    - confidence (si dispo)
    - inference_time_ms
    - model_uuid
    - model_version
    - timestamp
    """

    try:
        # Sélection du mode de chargement
        if run_id:
            model = load_model_from_run(run_id)
            model_version = run_id
        else:
            model = load_model_from_registry()
            model_version = "Production"

        # Préparation des données
        df = pd.DataFrame(
            [{"designation": designation, "description": description}]
        )

        # Prédiction
        start = time.time()
        raw_pred = model.predict(df)
        end = time.time()

        prediction_code = int(raw_pred[0])
        label = LABEL_MAPPING.get(prediction_code, str(prediction_code))

        # Probabilités si disponibles
        confidence = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(df)
            confidence = float(proba.max())

        # Construction de la réponse complète
        return {
            "prediction_code": prediction_code,
            "label": label,
            "run_id": run_id,
            "confidence": confidence,
            "inference_time_ms": round((end - start) * 1000, 3),
            "model_uuid": "unknown",
            "model_version": model_version,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except Exception as exc:
        raise RuntimeError(f"Erreur lors de la prédiction : {exc}")
