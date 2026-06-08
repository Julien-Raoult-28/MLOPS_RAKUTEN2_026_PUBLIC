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

from src.utils.mlflow_config import get_tracking_uri


# ---------------------------------------------------------------------------
# Cache mémoire des modèles
# ---------------------------------------------------------------------------
# Sans ce cache, chaque requête HTTP rechargeait le modèle depuis MLflow
# (désérialisation + I/O) : latence de plusieurs secondes et RAM instable.
# Ici, chaque modèle (Production ou run_id) n'est chargé qu'UNE fois puis
# réutilisé pour toutes les requêtes suivantes.
_MODEL_CACHE: dict[str, object] = {}

_PRODUCTION_KEY = "@production"


def load_model_from_registry() -> object:
    """
    Charge le modèle MLflow en stage 'Production' depuis le Model Registry.

    Le modèle est mis en cache après le premier chargement.

    Returns
    -------
    object
        Modèle MLflow chargé (pyfunc).
    """
    if _PRODUCTION_KEY in _MODEL_CACHE:
        return _MODEL_CACHE[_PRODUCTION_KEY]

    mlflow.set_tracking_uri(get_tracking_uri())
    model_uri = "models:/rakuten_classifier@production"

    try:
        model = mlflow.pyfunc.load_model(model_uri)
    except Exception as exc:
        raise RuntimeError(
            f"Erreur lors du chargement du modèle en Production : {exc}"
        )

    _MODEL_CACHE[_PRODUCTION_KEY] = model
    return model


def load_model_from_run(run_id: str) -> object:
    """
    Charge un modèle MLflow spécifique à partir d’un run_id.

    Le modèle est mis en cache (clé = run_id) après le premier chargement.

    Parameters
    ----------
    run_id : str
        Identifiant MLflow du run contenant le modèle.

    Returns
    -------
    object
        Modèle MLflow chargé (pyfunc).
    """
    if run_id in _MODEL_CACHE:
        return _MODEL_CACHE[run_id]

    mlflow.set_tracking_uri(get_tracking_uri())
    model_uri = f"runs:/{run_id}/model"

    try:
        model = mlflow.pyfunc.load_model(model_uri)
    except Exception as exc:
        raise RuntimeError(
            f"Erreur lors du chargement du modèle pour run_id={run_id} : {exc}"
        )

    _MODEL_CACHE[run_id] = model
    return model


def clear_model_cache() -> None:
    """Vide le cache des modèles (utile pour les tests ou un rechargement forcé)."""
    _MODEL_CACHE.clear()
