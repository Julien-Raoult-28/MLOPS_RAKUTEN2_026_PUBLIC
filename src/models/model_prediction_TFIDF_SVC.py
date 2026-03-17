# ============================================================
# IMPORTS
# ============================================================
import pandas as pd
import numpy as np
import joblib
import re

import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from src.features.text_features import (
    get_designation,
    get_description,
    first_words_series,
    numbers_units_series
)

# ============================================================
# MLflow
# ============================================================

mlflow.set_experiment("rakuten_classification")

# ============================================================
# 1) Chargement des données
# ============================================================

X_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\data\raw\X_train_update.csv"
Y_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\data\processed\Y_train_encode.csv"

X = pd.read_csv(X_path)
Y = pd.read_csv(Y_path)

df = X.merge(Y, on="Unnamed: 0")

y = df["prdtypecode_encoded"]
X = df.drop(columns=["prdtypecode_encoded"])

# ============================================================
# 2) Pipeline
# ============================================================

word_tfidf_designation = TfidfVectorizer(
    max_features=50000,
    ngram_range=(1,2),
    strip_accents="unicode",
    lowercase=True,
    sublinear_tf=True
)

word_tfidf_description = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1,2),
    strip_accents="unicode",
    lowercase=True,
    sublinear_tf=True
)

char_tfidf_designation = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3,5),
    min_df=2,
    lowercase=True
)

char_tfidf_description = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3,6),
    min_df=3,
    lowercase=True
)

features = ColumnTransformer([

 ("designation_word",
 Pipeline([
     ("select", FunctionTransformer(get_designation, validate=False)),
     ("tfidf", word_tfidf_designation)
 ]),
 ["designation"]),

("designation_char",
 Pipeline([
     ("select", FunctionTransformer(get_designation, validate=False)),
     ("tfidf", char_tfidf_designation)
 ]),
 ["designation"]),

("description_word",
 Pipeline([
     ("select", FunctionTransformer(get_description, validate=False)),
     ("tfidf", word_tfidf_description)
 ]),
 ["description"]),

("description_char",
 Pipeline([
     ("select", FunctionTransformer(get_description, validate=False)),
     ("tfidf", char_tfidf_description)
 ]),
 ["description"]),

("first_words",
 Pipeline([
     ("extract", FunctionTransformer(first_words_series, validate=False)),
     ("tfidf", TfidfVectorizer())
 ]),
 ["designation"]),

("numbers_units",
 Pipeline([
     ("extract", FunctionTransformer(numbers_units_series, validate=False)),
     ("tfidf", TfidfVectorizer())
 ]),
 ["designation"]),
])

pipe = Pipeline([
    ("features", features),
    ("clf", LinearSVC(C=1, class_weight="balanced", max_iter=20000, random_state=42))
])

# ============================================================
# 3) ENTRAINEMENT + MLFLOW
# ============================================================

with mlflow.start_run():

    print("==> Entraînement final sur toutes les données...")
    pipe.fit(X, y)
    print("✅ Modèle entraîné")

    # 👉 Log des paramètres
    mlflow.log_param("model", "LinearSVC")
    mlflow.log_param("C", 1)
    mlflow.log_param("max_iter", 20000)

    # ⚠️ Pas de métrique ici car pas de validation
    # (tu pourras en ajouter plus tard avec un train/val)

    # 👉 Sauvegarde classique (.pkl)
    model_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\models\1.3_rakuten_model_final.pkl"
    joblib.dump(pipe, model_path, compress=3)
    print("✅ Modèle final sauvegardé :", model_path)

    # 👉 Sauvegarde MLflow
    mlflow.sklearn.log_model(pipe, "model")

    print("✅ Modèle loggé dans MLflow")