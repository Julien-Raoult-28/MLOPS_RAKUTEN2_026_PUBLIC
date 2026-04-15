
"""
Script d'entraînement du modèle TF-IDF + LinearSVC avec suivi MLflow.

Étapes :
1. Chargement des données
2. Prétraitement et extraction de caractéristiques textuelles
3. Construction du pipeline TF-IDF + LinearSVC
4. Séparation train/validation
5. Entraînement du modèle
6. Calcul des métriques
7. Sauvegarde locale du modèle
8. Logging complet dans MLflow (params, metrics, artifacts, modèle)

Ce script est :
- reproductible
- portable
- compatible Docker / Airflow
- conforme aux bonnes pratiques MLOps
"""

# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

import matplotlib.pyplot as plt
import seaborn as sns
import io

import mlflow
import mlflow.sklearn

from src.features.text_features import (
    get_designation,
    get_description,
    first_words_series,
    numbers_units_series,
)

# ============================================================
# CONFIGURATION MLFLOW
# ============================================================

mlflow.set_tracking_uri(
    "sqlite:///C:/Users/angel/Desktop/A/Datascientest/Projet MLOps/FEV26-CMLOPS-RAKUTEN/mlflow.db"
)
mlflow.set_experiment("rakuten_classification")

BASE_DIR = Path(__file__).resolve().parents[2]

# ============================================================
# MODE RAPIDE (FAST MODE)
# ============================================================

FAST_MODE = False  # Passer à True pour un entraînement rapide (moins de données, moins de features)

MAX_FEATURES_WORD = 500 if FAST_MODE else 20000
MAX_FEATURES_DESC = 800 if FAST_MODE else 30000
MAX_ITER_SVC = 500 if FAST_MODE else 20000
SAMPLE_SIZE = 2000 if FAST_MODE else None

# ============================================================
# 1) Chargement des données
# ============================================================

def load_data():
    x_path = BASE_DIR / "data" / "raw" / "X_train_update.csv"
    y_path = BASE_DIR / "data" / "processed" / "Y_train_encode.csv"

    df_x = pd.read_csv(x_path)
    df_y = pd.read_csv(y_path)

    df = df_x.merge(df_y, on="Unnamed: 0")

    if SAMPLE_SIZE:
        df = df.sample(SAMPLE_SIZE, random_state=42)

    y = df["prdtypecode_encoded"]
    X = df.drop(columns=["prdtypecode_encoded"])

    return X, y

# ============================================================
# 2) Construction du pipeline
# ============================================================

def build_pipeline():

    word_tfidf_designation = TfidfVectorizer(
        max_features=MAX_FEATURES_WORD,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=True,
        sublinear_tf=True,
        min_df=5,
        max_df=0.8,
        dtype=np.float32,
    )

    word_tfidf_description = TfidfVectorizer(
        max_features=MAX_FEATURES_DESC,
        ngram_range=(1, 2),
        strip_accents="unicode",
        lowercase=True,
        sublinear_tf=True,
        min_df=5,
        max_df=0.8,
        dtype=np.float32,
    )

    char_tfidf_designation = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        lowercase=True,
    )

    char_tfidf_description = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 6),
        min_df=3,
        lowercase=True,
    )

    features = ColumnTransformer(
        [
            ("designation_word",
             Pipeline([
                 ("select", FunctionTransformer(get_designation, validate=False)),
                 ("tfidf", word_tfidf_designation),
             ]),
             ["designation"]),

            ("designation_char",
             Pipeline([
                 ("select", FunctionTransformer(get_designation, validate=False)),
                 ("tfidf", char_tfidf_designation),
             ]),
             ["designation"]),

            ("description_word",
             Pipeline([
                 ("select", FunctionTransformer(get_description, validate=False)),
                 ("tfidf", word_tfidf_description),
             ]),
             ["description"]),

            ("description_char",
             Pipeline([
                 ("select", FunctionTransformer(get_description, validate=False)),
                 ("tfidf", char_tfidf_description),
             ]),
             ["description"]),

            ("first_words",
             Pipeline([
                 ("extract", FunctionTransformer(first_words_series, validate=False)),
                 ("tfidf", TfidfVectorizer()),
             ]),
             ["designation"]),

            ("numbers_units",
             Pipeline([
                 ("extract", FunctionTransformer(numbers_units_series, validate=False)),
                 ("tfidf", TfidfVectorizer()),
             ]),
             ["designation"]),
        ]
    )

    pipeline = Pipeline(
        [
            ("features", features),
            ("clf", LinearSVC(
                C=1,
                class_weight="balanced",
                max_iter=MAX_ITER_SVC,
                random_state=42,
            )),
        ]
    )

    return pipeline

# ============================================================
# 3) Fonction principale d'entraînement
# ============================================================

def train():
    print("📥 Chargement des données...")
    X, y = load_data()

    print("✂️ Séparation train/validation...")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🔧 Construction du pipeline...")
    pipeline = build_pipeline()

    print("🚀 Début de l'entraînement...")
    with mlflow.start_run():

        mlflow.set_tag("mode", "FAST" if FAST_MODE else "FULL")
        mlflow.set_tag("model_type", "LinearSVC")

        pipeline.fit(X_train, y_train)

        print("📊 Évaluation...")
        y_pred = pipeline.predict(X_val)

        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, average="weighted")
        precision = precision_score(y_val, y_pred, average="weighted")
        recall = recall_score(y_val, y_pred, average="weighted")

        print(f"Accuracy : {acc:.4f}")
        print(f"F1-score : {f1:.4f}")

        # ============================================================
        # LOG PARAMS
        # ============================================================
        mlflow.log_param("C", 1)
        mlflow.log_param("max_iter", MAX_ITER_SVC)
        mlflow.log_param("max_features_word", MAX_FEATURES_WORD)
        mlflow.log_param("max_features_desc", MAX_FEATURES_DESC)
        mlflow.log_param("sample_size", SAMPLE_SIZE)

        # ============================================================
        # LOG METRICS
        # ============================================================
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision_weighted", precision)
        mlflow.log_metric("recall_weighted", recall)

        # ============================================================
        # CONFUSION MATRIX (PNG)
        # ============================================================
        cm = confusion_matrix(y_val, y_pred)

        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=False, cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("True")

        mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
        plt.close()

        # ============================================================
        # CLASSIFICATION REPORT (TXT)
        # ============================================================
        report = classification_report(y_val, y_pred)
        report_path = BASE_DIR / "models" / "classification_report.txt"

        with open(report_path, "w") as f:
            f.write(report)

        mlflow.log_artifact(report_path)

        # ============================================================
        # MODEL CARD (TXT)
        # ============================================================
        model_card_path = BASE_DIR / "models" / "model_card.txt"
        with open(model_card_path, "w") as f:
            f.write("Model: TF-IDF + LinearSVC\n")
            f.write(f"Mode: {'FAST' if FAST_MODE else 'FULL'}\n")
            f.write(f"Accuracy: {acc:.4f}\n")
            f.write(f"F1-score: {f1:.4f}\n")
            f.write("Description: Baseline text classification model.\n")
            f.write("Limitations: No deep learning, no embeddings.\n")

        mlflow.log_artifact(model_card_path)

        # ============================================================
        # PIPELINE SUMMARY (TXT)
        # ============================================================
        pipeline_path = BASE_DIR / "models" / "pipeline_summary.txt"
        with open(pipeline_path, "w") as f:
            f.write(str(pipeline))

        mlflow.log_artifact(pipeline_path)

        # ============================================================
        # SAVE MODEL
        # ============================================================
        model_path = BASE_DIR / "models" / "model_tfidf_svc.pkl"
        joblib.dump(pipeline, model_path)

        mlflow.sklearn.log_model(pipeline, "model")

        print("✅ Modèle sauvegardé et loggé dans MLflow.")

# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    train()