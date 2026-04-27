import typer
import mlflow
import pandas as pd

from src.models.train import train
from src.models.evaluate import evaluate
from src.utils.mlflow_config import get_tracking_uri

app = typer.Typer(help="CLI complet pour le pipeline MLOps Rakuten")


@app.command()
def train_cmd(mode: str = typer.Option("fast", help="Mode d'entraînement : fast ou full")):
    """
    Lance l'entraînement du modèle en mode FAST ou FULL.
    """
    # ❗ Pas de set_tracking_uri ici : c'est train() qui s'en charge
    #    en lisant MLFLOW_TRACKING_URI depuis l'environnement (.env / Docker).
    # ❗ Pas de start_run ici non plus : c'est train() qui ouvre le run.
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
    # URI lue via le helper partagé (src/utils/mlflow_config.py).
    mlflow.set_tracking_uri(get_tracking_uri())
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    X = pd.DataFrame([{
        "designation": designation,
        "description": description
    }])

    prediction = model.predict(X)[0]
    typer.echo(f"Prédiction : {prediction}")


if __name__ == "__main__":
    app()
