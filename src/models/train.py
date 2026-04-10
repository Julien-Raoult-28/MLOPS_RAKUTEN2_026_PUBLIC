"""
Module d'entraînement du modèle TF-IDF + LinearSVC avec suivi MLflow.
Version modulaire + configuration YAML + compatible CLI.

Étapes :
1. Chargement de la configuration
2. Chargement des données
3. Construction du pipeline
4. Séparation train/validation
5. Entraînement
6. Évaluation
7. Logging MLflow (params, metrics, artifacts, modèle)
"""

# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)

from src.utils.config_loader import load_config
from src.data.load_data import load_data
from src.models.pipeline import build_pipeline


# ============================================================
# FONCTION PRINCIPALE D'ENTRAÎNEMENT
# ============================================================

def train(mode: str = None):
    """
    Entraîne le modèle selon le mode (fast/full) et logge tout dans MLflow.
    """

    # --------------------------------------------------------
    # 1) Charger la configuration
    # --------------------------------------------------------
    config = load_config()

    if mode:
        config["mode"] = mode

    print(f"🚀 Mode d'entraînement : {config['mode'].upper()}")

    # --------------------------------------------------------
    # CONFIG MLflow — CORRECTION MAJEURE
    # --------------------------------------------------------
    # On force MLflow à utiliser le dossier mlruns/ comme tracking URI
    # (et non mlflow.db)
    BASE_DIR = Path(__file__).resolve().parents[2]
    mlruns_path = BASE_DIR / "mlruns"

    mlflow.set_tracking_uri(f"file:///{mlruns_path.as_posix()}")
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    # --------------------------------------------------------
    # 2) Chargement des données
    # --------------------------------------------------------
    print("📥 Chargement des données...")
    X, y = load_data(config)

    # --------------------------------------------------------
    # 3) Séparation train/validation
    # --------------------------------------------------------
    print("✂️ Séparation train/validation...")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --------------------------------------------------------
    # 4) Construction du pipeline
    # --------------------------------------------------------
    print("🔧 Construction du pipeline...")
    pipeline = build_pipeline(config)

    # --------------------------------------------------------
    # 5) Entraînement + MLflow
    # --------------------------------------------------------
    print("🚀 Début de l'entraînement...")

    with mlflow.start_run():

        mlflow.set_tag("mode", config["mode"])
        mlflow.set_tag("model_type", "LinearSVC")

        pipeline.fit(X_train, y_train)

        # ----------------------------------------------------
        # 6) Évaluation
        # ----------------------------------------------------
        print("📊 Évaluation...")
        y_pred = pipeline.predict(X_val)

        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, average="weighted")
        precision = precision_score(y_val, y_pred, average="weighted")
        recall = recall_score(y_val, y_pred, average="weighted")

        print(f"Accuracy : {acc:.4f}")
        print(f"F1-score : {f1:.4f}")

        # ----------------------------------------------------
        # 7) Logging MLflow
        # ----------------------------------------------------

        # PARAMS
        mlflow.log_param("C", config["model"]["C"])
        mlflow.log_param("mode", config["mode"])

        # METRICS
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision_weighted", precision)
        mlflow.log_metric("recall_weighted", recall)

        # ----------------------------------------------------
        # Artefact : Confusion Matrix
        # ----------------------------------------------------
        cm = confusion_matrix(y_val, y_pred)

        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=False, cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("True")

        mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
        plt.close()

        # ----------------------------------------------------
        # Artefact : Classification Report
        # ----------------------------------------------------
        report = classification_report(y_val, y_pred)
        report_path = BASE_DIR / "models" / "classification_report.txt"

        with open(report_path, "w") as f:
            f.write(report)

        mlflow.log_artifact(report_path)

        # ----------------------------------------------------
        # Artefact : Model Card
        # ----------------------------------------------------
        model_card_path = BASE_DIR / "models" / "model_card.txt"
        with open(model_card_path, "w") as f:
            f.write("Model: TF-IDF + LinearSVC\n")
            f.write(f"Mode: {config['mode']}\n")
            f.write(f"Accuracy: {acc:.4f}\n")
            f.write(f"F1-score: {f1:.4f}\n")

        mlflow.log_artifact(model_card_path)

        # ----------------------------------------------------
        # Artefact : Pipeline Summary
        # ----------------------------------------------------
        pipeline_path = BASE_DIR / "models" / "pipeline_summary.txt"
        with open(pipeline_path, "w") as f:
            f.write(str(pipeline))

        mlflow.log_artifact(pipeline_path)

        # ----------------------------------------------------
        # SAUVEGARDE DU MODÈLE — CORRECTION VALIDÉE
        # ----------------------------------------------------
        mlflow.sklearn.log_model(pipeline, "model")

        print("✅ Modèle sauvegardé et loggé dans MLflow.")


if __name__ == "__main__":
    train()