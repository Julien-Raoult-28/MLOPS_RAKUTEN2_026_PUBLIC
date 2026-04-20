import pandas as pd
from pathlib import Path

def load_data(config):
    base_dir = Path(__file__).resolve().parents[2]

    df_x = pd.read_csv(base_dir / config["data"]["raw_x"])
    df_y = pd.read_csv(base_dir / config["data"]["raw_y"])

    df = df_x.merge(df_y, on="Unnamed: 0")

    if config["mode"] == "fast":
        df = df.sample(config["data"]["sample_size_fast"], random_state=42)

    y = df["prdtypecode_encoded"]
    X = df.drop(columns=["prdtypecode_encoded"])

    return X, y