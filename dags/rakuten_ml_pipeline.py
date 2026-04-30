from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import json


# -----------------------
# PATHS
# -----------------------
RAW_X = "/opt/airflow/data/raw/X_train_update.csv"
RAW_Y = "/opt/airflow/data/processed/Y_train_encode.csv"
TMP = "/tmp/rakuten_clean.csv"
MODEL_PATH = "/opt/airflow/models/1.3_rakuten_model_final.pkl"


# -----------------------
# 1. LOAD
# -----------------------
def load_data():
    import pandas as pd

    x = pd.read_csv(RAW_X)
    y = pd.read_csv(RAW_Y)

    df = x.merge(y, on="Unnamed: 0")

    df = df[["designation", "description", "prdtypecode_encoded"]]

    # SAFE sampling (important)
    df = df.sample(n=min(50000, len(df)), random_state=42)

    df.to_csv(TMP, index=False)

    print("LOAD OK", df.shape)


# -----------------------
# 2. PREPROCESS
# -----------------------
def preprocess():
    import pandas as pd

    df = pd.read_csv(TMP)

    df["designation"] = df["designation"].fillna("").str.lower()
    df["description"] = df["description"].fillna("").str.lower()

    df["text"] = df["designation"] + " " + df["description"]

    df.to_csv(TMP, index=False)
    print("PREPROCESS OK")


# -----------------------
# 3. TRAIN
# -----------------------
def train():
    import pandas as pd
    import pickle
    import os

    from sklearn.svm import LinearSVC
    from sklearn.pipeline import FeatureUnion
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(TMP)

    X = df["text"]
    y = df["prdtypecode_encoded"]

    # ✅ SPLIT TRAIN / TEST
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    features = FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1,2), max_features=20000)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3,5), max_features=10000))
    ])

    # ✅ TRAIN uniquement sur TRAIN
    X_train_vec = features.fit_transform(X_train)

    model = LinearSVC(C=1.5, class_weight="balanced")
    model.fit(X_train_vec, y_train)

    os.makedirs("/opt/airflow/models", exist_ok=True)

    # ✅ on sauvegarde aussi le test pour evaluate
    with open("/opt/airflow/models/test_data.pkl", "wb") as f:
        pickle.dump((X_test, y_test), f)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((features, model), f)

    print("TRAIN OK")

def evaluate_model():
    import pickle
    import json
    from sklearn.metrics import accuracy_score, classification_report

    # load model
    with open(MODEL_PATH, "rb") as f:
        features, model = pickle.load(f)

    # load test data
    with open("/opt/airflow/models/test_data.pkl", "rb") as f:
        X_test, y_test = pickle.load(f)

    X_test_vec = features.transform(X_test)
    y_pred = model.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    metrics = {
        "accuracy": float(acc),
        "n_samples": len(y_test),
        "model": "LinearSVC",
        "report": report
    }

    with open("/opt/airflow/models/metrics.json", "w") as f:
        json.dump(metrics, f)

    print("EVALUATION OK:", acc)

# -----------------------
# DAG
# -----------------------
with DAG(
    dag_id="rakuten_ml_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="load", python_callable=load_data)
    t2 = PythonOperator(task_id="preprocess", python_callable=preprocess)
    t3 = PythonOperator(task_id="train", python_callable=train)
    t4 = PythonOperator(task_id="evaluate_model",python_callable=evaluate_model)

    t1 >> t2 >> t3 >> t4