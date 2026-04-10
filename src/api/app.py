from fastapi import FastAPI, HTTPException
from src.services.prediction_service import predict_product

app = FastAPI(
    title="Rakuten Product Classification API",
    description="API pour prédire la catégorie d'un produit Rakuten",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API Rakuten opérationnelle"}

@app.post("/predict")
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
        )
        return result

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {e}")