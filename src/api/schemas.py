"""
Schemas Pydantic utilisés par l'API Rakuten.

Ce module définit les modèles de données attendus par l'endpoint /predict.
Il est compatible avec Pydantic v2 et respecte les bonnes pratiques MLOps.

Points importants :
- Validation stricte des champs
- Nettoyage automatique des espaces (strip)
- run_id optionnel pour supporter le mode hybride (run_id + Model Registry)
- Documentation claire pour les débutants
"""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """
    Schéma d'entrée pour l'endpoint /predict.

    Ce modèle valide les données envoyées par l'utilisateur :
    - designation : nom court du produit
    - description : texte descriptif du produit
    - run_id : identifiant MLflow optionnel

    Fonctionnement hybride :
    - Si run_id est fourni → chargement du modèle associé au run MLflow.
    - Si run_id est absent → chargement du modèle en stage "Production"
      depuis le MLflow Model Registry.

    Le nettoyage des espaces est géré via json_schema_extra, car
    strip_whitespace est déprécié depuis Pydantic v2.
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

    run_id: str | None = Field(
        default=None,
        description=(
            "Optionnel : identifiant MLflow d'un run précis. "
            "Si absent, le modèle en Production du Model Registry sera utilisé."
        ),
    )
