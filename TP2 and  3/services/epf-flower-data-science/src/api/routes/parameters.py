from fastapi import APIRouter, HTTPException
from firestore_client import FirestoreClient



router = APIRouter()
firestore_client = FirestoreClient()


parameters_path = "/parameters/{collection_name}/{document_id}"



@router.get(parameters_path)
async def get_parameters(collection_name: str, document_id: str):
    try:
        parameters = firestore_client.get(collection_name, document_id)
        return parameters
    except FileExistsError as e:
        raise HTTPException(status_code=404, detail=str(e))
    




@router.post(parameters_path)
async def add_parameters(collection_name: str, document_id: str, parameters: dict):
    try:
        firestore_client.add(collection_name, document_id, parameters)
        return {"message": "Parameters added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




@router.put(parameters_path)
async def update_parameters(collection_name: str, document_id: str, parameters: dict):
    try:
        firestore_client.update(collection_name, document_id, parameters)
        return {"message": "Parameters updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
