import typer
from src.models.train import train
from src.models.evaluate import evaluate
import mlflow
import pandas as pd

app = typer.Typer(help="CLI complet pour le pipeline MLOps Rakuten")

# -----------------------------
# Commande : TRAIN
# -----------------------------
@app.command()
def train_cmd(mode: str = typer.Option("fast", help="Mode d'entraînement : fast ou full")):
    """
    Entraîne le modèle en mode FAST ou FULL.
    """
    train(mode=mode)


# -----------------------------
# Commande : EVALUATE
# -----------------------------
@app.command()
def evaluate_cmd(run_id: str = typer.Argument(..., help="ID du run MLflow à évaluer")):
    """
    Évalue un modèle MLflow existant.
    """
    evaluate(run_id=run_id)


# -----------------------------
# Commande : PREDICT
# -----------------------------
@app.command()
def predict_cmd(
    designation: str = typer.Option(..., help="Texte de la désignation"),
    description: str = typer.Option(..., help="Texte de la description"),
    run_id: str = typer.Option(..., help="Run ID du modèle MLflow à utiliser")
):
    """
    Fait une prédiction avec un modèle MLflow.
    """
    # ❗ IMPORTANT : on NE configure PAS MLflow ici
    # Le tracking_uri doit venir du config.yaml ou du service de prédiction
    # mlflow.set_tracking_uri("sqlite:///mlflow.db")  # ❌ supprimé

    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    X = pd.DataFrame([{
        "designation": designation,
        "description": description
    }])

    prediction = model.predict(X)[0]
    typer.echo(f"Prédiction : {prediction}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app()


# -----------------------------
# Commande : EVALUATE
# -----------------------------
@app.command()
def evaluate_cmd(run_id: str = typer.Argument(..., help="ID du run MLflow à évaluer")):
    """
    Évalue un modèle MLflow existant.
    """
    evaluate(run_id=run_id)


# -----------------------------
# Commande : PREDICT
# -----------------------------
@app.command()
def predict_cmd(
    designation: str = typer.Option(..., help="Texte de la désignation"),
    description: str = typer.Option(..., help="Texte de la description"),
    run_id: str = typer.Option(..., help="Run ID du modèle MLflow à utiliser")
):
    """
    Fait une prédiction avec un modèle MLflow.
    """
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    X = pd.DataFrame([{
        "designation": designation,
        "description": description
    }])

    prediction = model.predict(X)[0]
    typer.echo(f"Prédiction : {prediction}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app()