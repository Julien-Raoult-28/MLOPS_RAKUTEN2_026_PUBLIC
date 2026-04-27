"""
Script d'enregistrement d'un modèle dans le Model Registry MLflow.

Lance avec :
    python -m src.scripts.register_model

⚠️ Le serveur MLflow doit utiliser un backend qui supporte le Model Registry
   (SQLite, Postgres, MySQL — pas le mode "file:").
"""

import mlflow

from src.utils.mlflow_config import get_tracking_uri


def main() -> None:
    # 1. Tracking URI lue depuis l'environnement (.env / Docker), jamais hardcodée.
    mlflow.set_tracking_uri(get_tracking_uri())

    # 2. Paramètres
    run_id = "3cd771b4830740bf823fce572cea2e84"
    model_name = "rakuten_classifier"

    # 3. URI du modèle dans le run
    model_uri = f"runs:/{run_id}/model"

    print(">>> Enregistrement du modèle dans le Model Registry...")
    result = mlflow.register_model(model_uri=model_uri, name=model_name)

    version = result.version
    print(f">>> Modèle enregistré : version {version}")

    # 4. Promotion en Production
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Production"
    )

    print(f">>> Modèle promu en stage 'Production' (version {version})")


# Garde-fou : empêche l'exécution si quelqu'un fait `import src.scripts.register_model`.
# Le script ne s'exécute QUE quand lancé via `python -m src.scripts.register_model`.
if __name__ == "__main__":
    main()
