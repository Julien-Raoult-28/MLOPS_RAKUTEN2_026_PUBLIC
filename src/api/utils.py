"""
Fonctions utilitaires pour l’API Rakuten.

Ce module centralise le chargement des modèles MLflow afin de :
- séparer clairement la logique API de la logique MLOps,
- faciliter les tests unitaires,
- supporter le mode hybride (run_id ou Model Registry),
- garantir une architecture propre et maintenable.

Deux modes sont supportés :
1. Chargement du modèle en stage "Production" depuis le Model Registry.
2. Chargement d’un modèle spécifique à partir d’un run_id MLflow.
"""

import mlflow


def load_model_from_registry() -> object:
    """
    Charge le modèle MLflow en stage 'Production' depuis le Model Registry.

    Returns
    -------
    object
        Modèle MLflow chargé (pyfunc).
    """
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    model_uri = "models:/rakuten_classifier/Production"

    try:
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as exc:
        raise RuntimeError(
            f"Erreur lors du chargement du modèle en Production : {exc}"
        )


def load_model_from_run(run_id: str) -> object:
    """
    Charge un modèle MLflow spécifique à partir d’un run_id.

    Parameters
    ----------
    run_id : str
        Identifiant MLflow du run contenant le modèle.

    Returns
    -------
    object
        Modèle MLflow chargé (pyfunc).
    """
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    model_uri = f"runs:/{run_id}/model"

    try:
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as exc:
        raise RuntimeError(
            f"Erreur lors du chargement du modèle pour run_id={run_id} : {exc}"
        )
