import json
import pandas as pd
from pathlib import Path


def load_model_parameters():
    with open("src/config/model_parameters.json", "r") as f:
        return json.load(f)["LogisticRegression"]


def load_iris_data():
    file_path = Path(__file__).parent.parent / "api/routes/data/Iris.csv"
    df = pd.read_csv(file_path)
    return df