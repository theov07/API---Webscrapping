from firestore import FirestoreClient



firestore_client = FirestoreClient()

collection_name = "parameters"
document_id = "parameters"
data = {
    "n_estimators": 100,
    "criterion": "gini"
}

firestore_client.set(collection_name, document_id, data)