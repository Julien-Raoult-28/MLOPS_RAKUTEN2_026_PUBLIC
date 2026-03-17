# ============================================================
# IMPORTS
# ============================================================
import pandas as pd
import numpy as np
import joblib
import re

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# ============================================================
# 1) Chargement des données complètes
# ============================================================

X_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\data\raw\X_train_update.csv"
Y_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\data\processed\Y_train_encode.csv"

X = pd.read_csv(X_path)
Y = pd.read_csv(Y_path)

# Merge sur "Unnamed: 0"
df = X.merge(Y, on="Unnamed: 0")
print("Shape après merge :", df.shape)
print("Colonnes :", df.columns)

# ============================================================
# 2) Définir X et y
# ============================================================

y = df["prdtypecode_encoded"]  # target encodée
X = df.drop(columns=["prdtypecode_encoded"])

# ============================================================
# 3) TF-IDF et Feature Engineering
# ============================================================


from src.features.text_features import (
    get_designation,
    get_description,
    first_words_series,
    numbers_units_series
)

# ============================================================
# TF-IDF
# ============================================================

# ----------- WORD TF-IDF -----------

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


# ----------- CHAR TF-IDF -----------

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

# ============================================================
# COLUMN TRANSFORMER
# ============================================================

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

# Pipeline final
pipe = Pipeline([
    ("features", features),
    ("clf", LinearSVC(C=1, class_weight="balanced", max_iter=20000, random_state=42))
])

# ============================================================
# 4) Entraînement final
# ============================================================

print("==> Entraînement final sur toutes les données...")
pipe.fit(X, y)
print("✅ Modèle entraîné")

# ============================================================
# 5) Sauvegarde du modèle final
# ============================================================

model_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\models\1.3_rakuten_model_final.pkl"
joblib.dump(pipe, model_path, compress=3)
print("✅ Modèle final sauvegardé :", model_path)