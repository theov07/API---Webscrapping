from fastapi import APIRouter
import pandas as pd
from fastapi import APIRouter
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json
import joblib


router = APIRouter()

processed_data = None
X_train = None
X_test = None
y_train = None
y_test = None


def load_model_parameters():
    with open("src/config/model_parameters.json", "r") as f:
        return json.load(f)["parameters"]
    


@router.get("/load_data")
def load_data():
    df = pd.read_csv("src/api/routes/data/Iris.csv")
    return df.to_dict(orient="records")



@router.get("/process_data")
def process_data():

    global processed_data
    
    df = pd.read_csv("src/api/routes/data/Iris.csv")
    df = df.drop(columns=["Id"])

    df["Species"] = df["Species"].str.replace("Iris-", "", regex=False)

    if df is None:
        return {"error": "Les données doivent d'abord être traitées via /process_data."}
    

    encoder = LabelEncoder()
    df["Species_encoded"] = encoder.fit_transform(df["Species"])
    
    processed_data = df

    return {"message": "Données traitées"}




@router.get("/train_test_split")
def split_data():

    global processed_data, X_train, X_test, y_train, y_test

    if processed_data is None:
        return {"error": "Les données doivent d'abord être traitées via /process_data."}
    
    X = processed_data.drop(columns=["Species", "Species_encoded"])
    y = processed_data["Species_encoded"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return {
            "message": "Division effectuée",
            "X_train": X_train.values.tolist(),
            "X_test": X_test.values.tolist(),
            "y_train": y_train.tolist(),
            "y_test": y_test.tolist()
        }





@router.get("/train_model")
def train_model():
    global X_train, X_test, y_train, y_test
    
    if X_train is None or y_train is None:
        return {"error": "Les données doivent être divisées avant d'entraîner le modèle."}

    with open("src/config/model_parameters.json", "r") as f:
        params = json.load(f)["parameters"]
    
    model = LogisticRegression(
        penalty=params["penalty"],
        solver=params["solver"],
        max_iter=params["max_iter"],
        random_state=params["random_state"]
    )
    model.fit(X_train, y_train)
    
    joblib.dump(model, "src/models/logistic_regression_model.pkl")
    
    return {"message": "Modèle entraîné et sauvegardé"}





@router.get("/predict")
def predict():
    global X_test
    
    model = joblib.load("src/models/logistic_regression_model.pkl")
    
    y_pred = model.predict(X_test)

    return {"predictions": y_pred.tolist()}