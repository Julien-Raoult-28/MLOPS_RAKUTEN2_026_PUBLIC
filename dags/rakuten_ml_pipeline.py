"""
DAG : rakuten_ml_pipeline
-------------------------
Pipeline d'entraînement Rakuten orchestré par Airflow.

5 étapes (tâches) enchaînées :
    load → preprocess → train → evaluate_model → register_model

Ce que fait une exécution du DAG :
  1. lit les CSV bruts et écrit un CSV intermédiaire dans /tmp,
  2. crée un run MLflow (paramètres + métriques + artefact modèle),
  3. enregistre une nouvelle version dans le Model Registry,
  4. pose l'alias 'production' sur cette version → l'API la sert ensuite.

Le run_id MLflow circule entre les tâches via Airflow XCom (return value de
`train` récupérée par `evaluate_model` et `register_model`).

Le pipeline scikit-learn lui-même n'est PAS défini ici : il vient de
`src/models/pipeline.py` (fonction `build_pipeline`). Le DAG appelle cette
factory, ce qui évite de dupliquer la définition du modèle entre l'entraînement
en CLI et l'entraînement en DAG.
"""

import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


# -----------------------
# CONFIG
# -----------------------
RAW_X = "/opt/airflow/data/raw/X_train_update.csv"
RAW_Y = "/opt/airflow/data/processed/Y_train_encode.csv"
TMP = "/tmp/rakuten_clean.csv"
TEST_DATA_PATH = "/opt/airflow/models/test_data.pkl"
METRICS_PATH = "/opt/airflow/models/metrics.json"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:8080")
EXPERIMENT_NAME = "rakuten_ml_pipeline"
REGISTERED_MODEL_NAME = "rakuten_classifier"


# -----------------------
# 1. LOAD
# -----------------------
def load_data():
    import pandas as pd

    x = pd.read_csv(RAW_X)
    y = pd.read_csv(RAW_Y)

    df = x.merge(y, on="Unnamed: 0")
    df = df[["designation", "description", "prdtypecode_encoded"]]
    df = df.sample(n=min(50000, len(df)), random_state=42)

    df.to_csv(TMP, index=False)
    print("LOAD OK", df.shape)


# -----------------------
# 2. PREPROCESS
# -----------------------
def preprocess():
    """
    Remplace les NaN par "" sur les colonnes designation et description,
    puis ré-écrit le CSV intermédiaire.

    Le passage en minuscules n'est PAS fait ici : le pipeline scikit-learn
    (TfidfVectorizer, lowercase=True) s'en charge déjà. Le refaire ici serait
    un double traitement inutile (CPU gaspillé) sans aucun effet sur le modèle.
    """
    import pandas as pd

    df = pd.read_csv(TMP)
    df["designation"] = df["designation"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)

    df.to_csv(TMP, index=False)
    print("PREPROCESS OK")


# -----------------------
# 3. TRAIN
# -----------------------
def train(**context):
    import pickle

    import mlflow
    import mlflow.sklearn
    import pandas as pd
    from sklearn.model_selection import train_test_split

    # Import du pipeline partagé (factory) et de la config YAML
    from src.utils.config_loader import load_config
    from src.models.pipeline import build_pipeline

    config = load_config()
    mode = config["mode"]

    df = pd.read_csv(TMP)
    # Le pipeline attend un DataFrame avec ces 2 colonnes séparées
    # (et pas un texte déjà concaténé).
    X = df[["designation", "description"]]
    y = df["prdtypecode_encoded"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline(config)
    pipeline.fit(X_train, y_train)

    # Le modèle n'est PAS sauvegardé en .pkl local : il est déjà loggé dans
    # MLflow (mlflow.sklearn.log_model ci-dessous) et evaluate_model le
    # rechargera depuis MLflow via le run_id. On ne persiste localement que le
    # jeu de test, seul moyen de le passer à la tâche evaluate_model.
    os.makedirs("/opt/airflow/models", exist_ok=True)
    with open(TEST_DATA_PATH, "wb") as f:
        pickle.dump((X_test, y_test), f)

    # --- Envoi vers MLflow (format sklearn natif) ---
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    params = {
        "mode": mode,
        "C": config["model"]["C"],
        "max_iter": config["model"][f"max_iter_{mode}"],
        "max_features_word": config["model"][f"max_features_word_{mode}"],
        "max_features_desc": config["model"][f"max_features_desc_{mode}"],
        "test_size": 0.2,
        "random_state": 42,
        "n_samples_total": len(df),
        "n_samples_train": len(X_train),
        "n_samples_test": len(X_test),
    }

    with mlflow.start_run() as run:
        mlflow.set_tag("model_type", "LinearSVC")
        mlflow.set_tag("source", "airflow_dag")
        mlflow.log_params(params)
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            # On embarque le dossier src/ entier avec le modèle. Le pickle
            # du pipeline contient des références aux fonctions de
            # src/features/text_features.py ; sans le dossier, l'API qui
            # recharge le modèle tombe sur "ModuleNotFoundError: src.features".
            code_paths=["/opt/airflow/src"],
            input_example=X_train.head(2),
            # Crée la version directement dans le Model Registry (au lieu
            # de faire un client.create_model_version() dans une autre tâche).
            registered_model_name=REGISTERED_MODEL_NAME,
        )
        run_id = run.info.run_id

    print(f"TRAIN OK — MLflow run_id={run_id}")
    # Cette valeur est automatiquement stockée dans XCom et récupérable
    # depuis les tâches suivantes via ti.xcom_pull(task_ids="train").
    return run_id


# -----------------------
# 4. EVALUATE
# -----------------------
def evaluate_model(**context):
    import json
    import pickle

    import mlflow
    import mlflow.sklearn
    from sklearn.metrics import accuracy_score, classification_report

    ti = context["ti"]
    run_id = ti.xcom_pull(task_ids="train")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    # Le modèle est rechargé depuis MLflow (artefact du run) au lieu d'un .pkl
    # local : on évalue ainsi exactement l'artefact qui sera servi en prod.
    pipeline = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    with open(TEST_DATA_PATH, "rb") as f:
        X_test, y_test = pickle.load(f)

    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    metrics = {
        "accuracy": float(acc),
        "n_samples": len(y_test),
        "model": "LinearSVC",
        "report": report,
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f)

    with mlflow.start_run(run_id=run_id):
        mlflow.log_metrics({
            "accuracy": float(acc),
            "n_test_samples": len(y_test),
            "macro_f1": float(report["macro avg"]["f1-score"]),
            "weighted_f1": float(report["weighted avg"]["f1-score"]),
        })
        mlflow.log_artifact(METRICS_PATH, artifact_path="metrics")

    print(f"EVALUATION OK — accuracy={acc:.4f}")


# -----------------------
# 5. REGISTER MODEL
# -----------------------
def register_model(**context):
    """
    Pose l'alias 'production' sur la version qui vient d'être enregistrée
    par la tâche train (`registered_model_name=` dans log_model).

    Conséquence : l'API qui charge le modèle via
        models:/rakuten_classifier@production
    pointera automatiquement sur la nouvelle version au prochain reload.
    """
    import mlflow
    from mlflow.tracking import MlflowClient

    ti = context["ti"]
    run_id = ti.xcom_pull(task_ids="train")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    # On retrouve la version créée par log_model en filtrant sur le run_id.
    versions = client.search_model_versions(f"name='{REGISTERED_MODEL_NAME}'")
    matching = [v for v in versions if v.run_id == run_id]
    if not matching:
        raise RuntimeError(
            f"Aucune version trouvée pour run_id={run_id} dans "
            f"'{REGISTERED_MODEL_NAME}'. La tâche train a-t-elle bien enregistré ?"
        )
    mv = matching[0]
    print(f"FOUND VERSION: {mv.version} (run_id={mv.run_id})")

    # Bascule l'alias 'production' sur cette version. Si l'alias existait
    # déjà sur une autre version, MLflow le déplace (pas de doublon possible).
    client.set_registered_model_alias(
        name=REGISTERED_MODEL_NAME,
        alias="production",
        version=mv.version,
    )
    print(f"REGISTER OK — {REGISTERED_MODEL_NAME} v{mv.version} → @production")


# -----------------------
# DAG
# -----------------------
with DAG(
    dag_id="rakuten_ml_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id="load", python_callable=load_data)
    t2 = PythonOperator(task_id="preprocess", python_callable=preprocess)
    t3 = PythonOperator(task_id="train", python_callable=train)
    t4 = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)
    t5 = PythonOperator(task_id="register_model", python_callable=register_model)

    t1 >> t2 >> t3 >> t4 >> t5
