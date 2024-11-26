from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/load_data")
def load_data():
    df = pd.read_csv("src/api/routes/data/iris.csv")
    return df.to_dict(orient="records")


@router.get("/process_data")
def process_data():
    df = pd.read_csv("src/api/routes/data/iris.csv")
    # Effectuer des traitements ici
    return {"message": "Données traitées"}