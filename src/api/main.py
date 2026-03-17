# ============================================================
# IMPORTS
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# ============================================================
# LOAD LABEL MAPPING
# ============================================================

mapping_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\data\processed\Y_train_encode.csv"

mapping_df = pd.read_csv(mapping_path)

# garder uniquement les colonnes utiles + enlever doublons
mapping_df = mapping_df[["prdtypecode_encoded", "libelle_type_code"]].drop_duplicates()

# dictionnaire encodé -> libellé métier
label_map = dict(zip(
    mapping_df["prdtypecode_encoded"],
    mapping_df["libelle_type_code"]
))

print("✅ Mapping labels chargé")

# ============================================================
# INIT API
# ============================================================

app = FastAPI(
    title="Rakuten Product Classification API",
    description="API de prédiction de catégorie produit",
    version="1.0"
)


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\models\1.3_rakuten_model_final.pkl"

model = joblib.load(MODEL_PATH)

print("✅ Modèle chargé")


# ============================================================
# SCHEMA INPUT
# ============================================================

class Product(BaseModel):
    designation: str
    description: str


# ============================================================
# ROUTES
# ============================================================

@app.get("/")
def home():
    return {"message": "API Rakuten OK"}


@app.post("/predict")
def predict(product: Product):

    df = pd.DataFrame([{
        "designation": product.designation,
        "description": product.description
    }])

    prediction = model.predict(df)[0]

    label = label_map.get(prediction, "unknown")

    return {
    "prediction_encoded": int(prediction),
    "label": label,
    "input": product.designation[:50]  # debug léger
}