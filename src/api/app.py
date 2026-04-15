<<<<<<< Updated upstream
from fastapi import FastAPI, HTTPException
from src.services.prediction_service import predict_product
=======
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

# ---------------------------------------------------------------------------
# Configuration API
# ---------------------------------------------------------------------------

API_TOKEN = "RAKUTEN_SECRET_123"
>>>>>>> Stashed changes

app = FastAPI(
    title="Rakuten Product Classification API",
    description="API pour prédire la catégorie d'un produit Rakuten",
    version="1.0.0",
)

<<<<<<< Updated upstream
=======

# ---------------------------------------------------------------------------
# Middleware de sécurité
# ---------------------------------------------------------------------------

def verify_token(x_token: str = Header(None)) -> None:
    """
    Vérifie la présence et la validité du token API.

    Paramètres
    ----------
    x_token : str
        Token transmis dans l'en-tête HTTP.

    Exceptions
    ----------
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

>>>>>>> Stashed changes
@app.get("/")
def root() -> dict:
    """
    Endpoint de santé (healthcheck).

    Retour
    ------
    dict
        Message confirmant que l'API est opérationnelle.
    """
    return {"message": "API Rakuten opérationnelle"}

@app.post("/predict")
<<<<<<< Updated upstream
def predict_endpoint(
    designation: str,
    description: str,
    run_id: str
):
    """
    Endpoint minimaliste pour prédire la catégorie d'un produit.
    """
    try:
        result = predict_product(
            designation=designation,
            description=description,
            run_id=run_id
=======
def predict(request: PredictionRequest, x_token: str = Header(None)) -> dict:
    """
    Endpoint principal : prédire la catégorie d'un produit.

    Paramètres
    ----------
    request : PredictionRequest
        Données d'entrée validées par Pydantic.
    x_token : str
        Token API transmis dans l'en-tête HTTP.

    Retour
    ------
    dict
        Résultat structuré contenant la prédiction et les métadonnées.

    Exceptions
    ----------
    HTTPException
        - 401 si token invalide
        - 500 si erreur interne (MLflow, modèle, etc.)
    """
    verify_token(x_token)

    try:
        result = predict_product(
            designation=request.designation,
            description=request.description,
            run_id=request.run_id,
>>>>>>> Stashed changes
        )
        return result

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

<<<<<<< Updated upstream
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {e}")
=======
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors de la prédiction : {exc}",
        )
>>>>>>> Stashed changes
