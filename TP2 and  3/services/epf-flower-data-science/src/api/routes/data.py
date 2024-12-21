from src.services.data import load_iris_data
from src.services.cleaning import preprocess_data
from fastapi import APIRouter


router = APIRouter()


@router.get("/load_data")
def load_data():
    df = load_iris_data()
    return df.to_dict(orient="records")



@router.get("/process_data")
def process_data():
    df = load_iris_data()
    df = preprocess_data(df)
    return {"message": "Données traitées", "processed_data": df.to_dict(orient="records")}