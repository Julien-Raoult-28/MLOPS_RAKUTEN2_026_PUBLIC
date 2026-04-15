"""
Application FastAPI pour la classification de produits Rakuten.

Cette API expose un endpoint /predict permettant :
- soit d'utiliser un modèle MLflow spécifique via un run_id,
- soit d'utiliser automatiquement le modèle en stage "Production"
  du MLflow Model Registry si aucun run_id n'est fourni.

La sécurité est assurée par un token transmis dans l'en-tête HTTP.
"""

from fastapi import FastAPI, HTTPException, Header
from src.services.prediction_service import predict_product
from src.api.schemas import PredictionRequest

API_TOKEN = "RAKUTEN_SECRET_123"

app = FastAPI(
    title="Rakuten Product Classification API",
    description="API pour prédire la catégorie d'un produit Rakuten",
    version="1.0.0",
)

def verify_token(x_token: str = Header(None)) -> None:
    """Vérifie la présence et la validité du token API."""
    if x_token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou manquant",
        )

@app.get("/")
def root() -> dict:
    """Endpoint de santé (healthcheck)."""
    return {"message": "API Rakuten opérationnelle"}

@app.post("/predict")
def predict(request: PredictionRequest, x_token: str = Header(None)) -> dict:
    """
    Endpoint principal : prédire la catégorie d'un produit.
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
