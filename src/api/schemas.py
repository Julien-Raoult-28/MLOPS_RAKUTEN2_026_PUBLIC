"""
Schemas Pydantic utilisés par l'API Rakuten.

Ce module définit les modèles de données attendus par l'endpoint /predict.
Il est compatible avec Pydantic v2 et respecte les bonnes pratiques MLOps.

Points importants :
- Validation stricte des champs
- Nettoyage automatique des espaces (strip)
- run_id optionnel pour supporter le mode hybride (run_id + Model Registry)
- Schéma de sortie structuré pour la traçabilité
"""

from pydantic import BaseModel, Field
from typing import Optional


class PredictionRequest(BaseModel):
    """
    Schéma d'entrée pour l'endpoint /predict.

    - designation : nom court du produit
    - description : texte descriptif du produit
    - run_id : identifiant MLflow optionnel

    Fonctionnement hybride :
    - Si run_id est fourni → modèle du run MLflow
    - Si run_id est absent → modèle en Production du Model Registry
    """

    designation: str = Field(
        ...,
        min_length=2,
        json_schema_extra={"strip_whitespace": True},
        description="Nom court du produit (min. 2 caractères).",
    )

    description: str = Field(
        ...,
        min_length=5,
        json_schema_extra={"strip_whitespace": True},
        description="Description textuelle du produit (min. 5 caractères).",
    )

    run_id: Optional[str] = Field(
        default=None,
        description=(
            "Optionnel : identifiant MLflow d'un run précis. "
            "Si absent, le modèle en Production du Model Registry sera utilisé."
        ),
    )


class PredictionResponse(BaseModel):
    """
    Schéma de sortie pour l'endpoint /predict.

    Champs renvoyés :
    - prediction_code : code numérique de la classe prédite
    - label : libellé métier décodé
    - run_id : identifiant du modèle utilisé (None → Production)
    - confidence : probabilité si disponible
    - inference_time_ms : temps d'inférence en millisecondes
    - model_uuid : identifiant interne du modèle
    - model_version : version MLflow (Production ou run_id)
    - timestamp : horodatage ISO
    """

    prediction_code: int
    label: str
    run_id: Optional[str]
    confidence: Optional[float]
    inference_time_ms: float
    model_uuid: str
    model_version: str
    timestamp: str
