from fastapi import APIRouter, HTTPException
import pandas as pd
from fastapi import APIRouter
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json
import joblib
import os
from typing import List
from firestore_client import FirestoreClient  # Updated import statement
from pathlib import Path
import sys

# services_path = Path(__file__).parent.parent / "services"
# sys.path.append(str(services_path))


from src.services.data import load_iris_data, load_model_parameters
from src.services.cleaning import preprocess_data
from src.services.modele import split_data, train_model, evaluate_model



firestore_client = FirestoreClient()
router = APIRouter()


processed_data = None
X_train = None
X_test = None
y_train = None
y_test = None





@router.get("/load_data")
def load_data():
    df = load_iris_data()
    return df.to_dict(orient="records")




@router.get("/process_data")
def process_data():
    df = load_iris_data()
    df = preprocess_data(df)
    return {"message": "Données traitées", "processed_data": df.to_dict(orient="records")}




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






@router.get("/parameters/{collection_name}/{document_id}")
async def get_parameters(collection_name: str, document_id: str):
    try:
        parameters = firestore_client.get(collection_name, document_id)
        return parameters
    except FileExistsError as e:
        raise HTTPException(status_code=404, detail=str(e))
    






@router.post("/parameters/{collection_name}/{document_id}")
async def add_parameters(collection_name: str, document_id: str, parameters: dict):
    try:
        firestore_client.add(collection_name, document_id, parameters)
        return {"message": "Parameters added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




@router.put("/parameters/{collection_name}/{document_id}")
async def update_parameters(collection_name: str, document_id: str, parameters: dict):
    try:
        firestore_client.update(collection_name, document_id, parameters)
        return {"message": "Parameters updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
