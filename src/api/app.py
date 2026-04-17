"""
Application FastAPI pour la classification de produits Rakuten.

Cette API expose un endpoint /predict permettant deux modes :
- Mode RUN : l’utilisateur fournit un run_id MLflow → chargement du modèle associé.
- Mode REGISTRY : aucun run_id → chargement automatique du modèle en stage
  "Production" depuis le MLflow Model Registry.

La sécurité est assurée par un token transmis dans l’en-tête HTTP.
"""

from fastapi import FastAPI, HTTPException, Header
from src.services.prediction_service import predict_product
from src.api.schemas import PredictionRequest, PredictionResponse

# ---------------------------------------------------------------------------
# Configuration API
# ---------------------------------------------------------------------------

API_TOKEN = "RAKUTEN_SECRET_123"

app = FastAPI(
    title="Rakuten Product Classification API",
    description=(
        "API permettant de prédire la catégorie d’un produit Rakuten "
        "à partir de sa désignation et de sa description. "
        "Compatible avec MLflow Model Registry et mode hybride."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Middleware de sécurité
# ---------------------------------------------------------------------------

def verify_token(x_token: str = Header(None)) -> None:
    """
    Vérifie la présence et la validité du token API.

    Parameters
    ----------
    x_token : str
        Token transmis dans l’en-tête HTTP.

    Raises
    ------
    HTTPException
        Si le token est absent ou incorrect.
    """
    if x_token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou manquant",
        )

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def root() -> dict:
    """
    Endpoint de santé (healthcheck).

    Returns
    -------
    dict
        Message confirmant que l’API fonctionne.
    """
    return {"message": "API Rakuten opérationnelle"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, x_token: str = Header(None)) -> dict:
    """
    Endpoint principal : prédire la catégorie d’un produit.

    Parameters
    ----------
    request : PredictionRequest
        Données d’entrée validées par Pydantic.
    x_token : str
        Token API transmis dans l’en-tête HTTP.

    Returns
    -------
    dict
        Résultat structuré contenant la prédiction, la confiance,
        les métadonnées du modèle et le timestamp.

    Raises
    ------
    HTTPException
        - 401 si token invalide
        - 400 si erreur de validation
        - 500 si erreur interne (MLflow, modèle, etc.)
    """
    verify_token(x_token)

    try:
        return predict_product(
            designation=request.designation,
            description=request.description,
            run_id=request.run_id,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la prédiction : {exc}",
        )
