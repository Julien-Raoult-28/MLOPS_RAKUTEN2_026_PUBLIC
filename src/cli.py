import typer
import mlflow
from src.models.train import train
from src.models.evaluate import evaluate
import pandas as pd

app = typer.Typer(help="CLI complet pour le pipeline MLOps Rakuten")


@app.command()
def train_cmd(mode: str = typer.Option("fast", help="Mode d'entraînement : fast ou full")):
    """
    Lance l'entraînement du modèle en mode FAST ou FULL.
    """
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("rakuten_classification")

    # ❗ NE PAS ouvrir de run ici
    model = train(mode=mode)

    typer.echo("🎉 Entraînement terminé et modèle loggé dans MLflow.")


@app.command()
def evaluate_cmd(run_id: str = typer.Argument(..., help="ID du run MLflow à évaluer")):
    evaluate(run_id=run_id)


@app.command()
def predict_cmd(
    designation: str = typer.Option(...),
    description: str = typer.Option(...),
    run_id: str = typer.Option(...)
):
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    X = pd.DataFrame([{
        "designation": designation,
        "description": description
    }])

    prediction = model.predict(X)[0]
    typer.echo(f"Prédiction : {prediction}")


if __name__ == "__main__":
    app()
