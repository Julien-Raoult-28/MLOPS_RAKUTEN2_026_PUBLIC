"""
Module d'évaluation du modèle TF-IDF + LinearSVC.
Version modulaire + configuration YAML + compatible MLflow.

Étapes :
1. Chargement de la configuration
2. Chargement du modèle MLflow ou local
3. Chargement des données de test
4. Calcul des métriques
5. Logging MLflow (metrics + artifacts)
"""

# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns

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


# ============================================================
# FONCTION D'ÉVALUATION
# ============================================================

def evaluate(run_id: str = None):
    """
    Évalue un modèle MLflow ou local.
    - run_id : identifiant MLflow du modèle à charger
    """

    # --------------------------------------------------------
    # 1) Charger la configuration
    # --------------------------------------------------------
    config = load_config()

    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    BASE_DIR = Path(__file__).resolve().parents[2]

    # --------------------------------------------------------
    # 2) Charger les données (FAST ou FULL selon YAML)
    # --------------------------------------------------------
    print("📥 Chargement des données de test...")
    X, y = load_data(config)

    # --------------------------------------------------------
    # 3) Charger le modèle
    # --------------------------------------------------------
        # --------------------------------------------------------
    # 3) Charger le modèle
    # --------------------------------------------------------
    if run_id:
        print(f"📦 Chargement du modèle MLflow (run_id={run_id})...")
        model_uri = f"runs:/{run_id}/model"
        model = mlflow.sklearn.load_model(model_uri)
    else:
        print("❌ Aucun run_id fourni. Veuillez spécifier un modèle MLflow à évaluer.")
        return
    
    
    
    
    '''if run_id:
        print(f"📦 Chargement du modèle MLflow (run_id={run_id})...")
        model_uri = f"runs:/{run_id}/model"
        model = mlflow.sklearn.load_model(model_uri)
    else:
        print("📦 Chargement du modèle local...")
        model_path = BASE_DIR / "models" / "model_tfidf_svc.pkl"
        model = mlflow.sklearn.load_model(model_path)'''

    # --------------------------------------------------------
    # 4) Prédictions
    # --------------------------------------------------------
    print("🔮 Prédictions...")
    y_pred = model.predict(X)

    # --------------------------------------------------------
    # 5) Calcul des métriques
    # --------------------------------------------------------
    print("📊 Calcul des métriques...")

    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred, average="weighted")
    precision = precision_score(y, y_pred, average="weighted")
    recall = recall_score(y, y_pred, average="weighted")

    print(f"Accuracy : {acc:.4f}")
    print(f"F1-score : {f1:.4f}")

    # --------------------------------------------------------
    # 6) Logging MLflow
    # --------------------------------------------------------
    with mlflow.start_run(run_name="evaluation"):

        mlflow.log_metric("eval_accuracy", acc)
        mlflow.log_metric("eval_f1_score", f1)
        mlflow.log_metric("eval_precision_weighted", precision)
        mlflow.log_metric("eval_recall_weighted", recall)

        # ----------------------------------------------------
        # Confusion Matrix
        # ----------------------------------------------------
        cm = confusion_matrix(y, y_pred)

        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=False, cmap="Blues")
        plt.title("Confusion Matrix (Evaluation)")
        plt.xlabel("Predicted")
        plt.ylabel("True")

        mlflow.log_figure(plt.gcf(), "eval_confusion_matrix.png")
        plt.close()

        # ----------------------------------------------------
        # Classification Report
        # ----------------------------------------------------
        report = classification_report(y, y_pred)
        report_path = BASE_DIR / "models" / "eval_classification_report.txt"

        with open(report_path, "w") as f:
            f.write(report)

        mlflow.log_artifact(report_path)

        print("✅ Évaluation terminée et loggée dans MLflow.")