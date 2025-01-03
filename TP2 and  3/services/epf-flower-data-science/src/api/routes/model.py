from src.services.data import load_iris_data
from src.services.cleaning import preprocess_data
from src.services.modele import split_data, train_model, evaluate_model
from fastapi import APIRouter, HTTPException
import os
import pandas as pd
import joblib
from typing import List


router = APIRouter()


### Variable initialization ###

processed_data = None
X_train = None
X_test = None
y_train = None
y_test = None



@router.get("/train_test_split")
def split_data_route():
    df = preprocess_data(load_iris_data())
    X_train, X_test, y_train, y_test = split_data(df)
    return {
        "message": "Division effectuée",
        "X_train": X_train.values.tolist(),
        "X_test": X_test.values.tolist(),
        "y_train": y_train.tolist(),
        "y_test": y_test.tolist()
    }




@router.post("/train_model")
def train_model_route():
    df = preprocess_data(load_iris_data())
    X_train, X_test, y_train, y_test = split_data(df)
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)
    return {"message": "Modèle entraîné", "accuracy": accuracy}






@router.post("/predict")
def predict(data: List[dict]):
    try:
        model_path = "src/models/logistic_regression_model.pkl"
        if not os.path.exists(model_path):
            return {"error": "Le modèle entraîné est introuvable. Veuillez entraîner le modèle d'abord."}
        
        model = joblib.load(model_path)
        X_input = pd.DataFrame(data)
        predictions = model.predict(X_input)
        reverse_species_mapping = {0: "Iris-setosa", 1: "Iris-versicolor", 2: "Iris-virginica"}
        formatted_predictions = [
            f"{pred} ({reverse_species_mapping[pred]})" for pred in predictions
        ]
        return {"predictions": formatted_predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))