"""
Module d'entraînement du modèle TF-IDF + LinearSVC avec suivi MLflow.

Ce script implémente un pipeline d'entraînement complet, modulaire et
configurable via un fichier YAML. Il est compatible avec une exécution
en ligne de commande (CLI) et respecte les bonnes pratiques MLOps.
"""

from pathlib import Path
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


def train(mode: str = None):
    """
    Entraîne le modèle TF-IDF + LinearSVC selon le mode choisi (fast/full)
    et logge l'ensemble des artefacts dans MLflow + Model Registry.
    """

    # --------------------------------------------------------
    # 1) Chargement de la configuration
    # --------------------------------------------------------
    config = load_config()

    if mode:
        config["mode"] = mode

    print(f"🚀 Mode d'entraînement : {config['mode'].upper()}")

    # --------------------------------------------------------
    # 2) Configuration MLflow (SQLite + Experiment propre)
    # --------------------------------------------------------
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    base_dir = Path(__file__).resolve().parents[2]

    # --------------------------------------------------------
    # 3) Chargement des données
    # --------------------------------------------------------
    print("📥 Chargement des données...")
    X, y = load_data(config)

    # --------------------------------------------------------
    # 4) Séparation train/validation
    # --------------------------------------------------------
    print("✂️ Séparation train/validation...")
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # --------------------------------------------------------
    # 5) Construction du pipeline
    # --------------------------------------------------------
    print("🔧 Construction du pipeline...")
    pipeline = build_pipeline(config)

    # --------------------------------------------------------
    # 6) Entraînement + MLflow
    # --------------------------------------------------------
    print("🚀 Début de l'entraînement...")

    with mlflow.start_run() as run:

        mlflow.set_tag("mode", config["mode"])
        mlflow.set_tag("model_type", "LinearSVC")

        print(f"📌 run_id MLflow : {run.info.run_id}")

        pipeline.fit(X_train, y_train)

        # ----------------------------------------------------
        # 7) Évaluation
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
        # Logging MLflow : paramètres et métriques
        # ----------------------------------------------------
        mlflow.log_param("C", config["model"]["C"])
        mlflow.log_param("mode", config["mode"])

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision_weighted", precision)
        mlflow.log_metric("recall_weighted", recall)

        # ----------------------------------------------------
        # Artefact : matrice de confusion
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
        # Artefact : classification report
        # ----------------------------------------------------
        report = classification_report(y_val, y_pred)
        report_path = base_dir / "models" / "classification_report.txt"

        with open(report_path, "w") as f:
            f.write(report)

        mlflow.log_artifact(report_path)

        # ----------------------------------------------------
        # Artefact : model card
        # ----------------------------------------------------
        model_card_path = base_dir / "models" / "model_card.txt"
        with open(model_card_path, "w") as f:
            f.write("Model: TF-IDF + LinearSVC\n")
            f.write(f"Mode: {config['mode']}\n")
            f.write(f"Accuracy: {acc:.4f}\n")
            f.write(f"F1-score: {f1:.4f}\n")

        mlflow.log_artifact(model_card_path)

        # ----------------------------------------------------
        # Artefact : pipeline summary
        # ----------------------------------------------------
        pipeline_path = base_dir / "models" / "pipeline_summary.txt"
        with open(pipeline_path, "w") as f:
            f.write(str(pipeline))

        mlflow.log_artifact(pipeline_path)

        # ----------------------------------------------------
        # Sauvegarde du modèle + Model Registry
        # ----------------------------------------------------
        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="model",
            registered_model_name="rakuten_classifier"
        )

        print("✅ Modèle loggé dans le run + enregistré dans le Model Registry.")
        print(f"📌 Nouveau run_id (SQLite) : {run.info.run_id}")

        return pipeline
