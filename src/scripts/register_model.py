"""
Promotion d'une version du modèle 'rakuten_classifier' en production.

Lance avec :
    python -m src.scripts.register_model           # promeut la dernière version
    python -m src.scripts.register_model 3         # promeut la version 3

L'enregistrement initial dans le Model Registry est déjà fait par train.py
(via `registered_model_name=...` dans `mlflow.sklearn.log_model`). Ce script
se contente de poser l'alias 'production' sur la version choisie.

API utilisée : `set_registered_model_alias`. Les anciens "stages"
(Staging/Production) sont dépréciés et retirés dans MLflow 3.x.
"""

import argparse

import mlflow
from mlflow.tracking import MlflowClient

from src.utils.mlflow_config import get_tracking_uri


MODEL_NAME = "rakuten_classifier"
PRODUCTION_ALIAS = "production"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "version",
        nargs="?",
        type=int,
        default=None,
        help="Numéro de version à promouvoir. Si omis, la dernière est utilisée.",
    )
    args = parser.parse_args()

    mlflow.set_tracking_uri(get_tracking_uri())
    client = MlflowClient()

    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if not versions:
        raise RuntimeError(
            f"Aucune version trouvée pour le modèle '{MODEL_NAME}'. "
            f"Lance d'abord un entraînement (python -m src.models.train)."
        )

    if args.version is None:
        target = max(versions, key=lambda v: int(v.version))
        print(f">>> Dernière version trouvée : {target.version} (run_id={target.run_id})")
    else:
        target = next((v for v in versions if int(v.version) == args.version), None)
        if target is None:
            available = sorted(int(v.version) for v in versions)
            raise RuntimeError(
                f"Version {args.version} introuvable pour '{MODEL_NAME}'. "
                f"Versions disponibles : {available}"
            )
        print(f">>> Version demandée : {target.version} (run_id={target.run_id})")

    client.set_registered_model_alias(MODEL_NAME, PRODUCTION_ALIAS, target.version)
    print(f">>> Alias '{PRODUCTION_ALIAS}' posé sur la version {target.version}")
    print(f">>> Chargement possible via : models:/{MODEL_NAME}@{PRODUCTION_ALIAS}")


if __name__ == "__main__":
    main()
