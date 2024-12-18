import pytest
from fastapi.testclient import TestClient
from src.app import get_application

app = get_application()
client = TestClient(app)



def test_load_data():
    response = client.get("/load_data")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_process_data():
    response = client.get("/process_data")
    assert response.status_code == 200
    
    data = response.json()
    
    assert "message" in data
    assert "processed_data" in data



def test_split_data():
    response = client.get("/train_test_split")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "X_train" in data
    assert "X_test" in data
    assert "y_train" in data
    assert "y_test" in data



def test_train_model():
    response = client.post("/train_model")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data



def test_predict():
    sample_data = [
        
        {"SepalLengthCm": 5.1, 
         "SepalWidthCm": 3.5, "PetalLengthCm": 1.4, 
         "PetalWidthCm": 0.2},

        {"SepalLengthCm": 7.0, "SepalWidthCm": 3.2, 
         "PetalLengthCm": 4.7, "PetalWidthCm": 1.4}
    ]
    
    response = client.post("/predict", json=sample_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "predictions" in data



def test_get_parameters():
    response = client.get("/parameters/parameters2/parameters2_document")
    assert response.status_code in [200, 404]



def test_add_parameters():
    parameters = {"Random_forest": "gain", 
                "n_estimators": 100}
    
    response = client.post("/parameters/parameters2/parameters2_document", json=parameters)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data



def test_update_parameters():
    parameters = {"Random_forest": "gain", 
             "n_estimators": 200}
    
    response = client.put("/parameters/parameters2/parameters2_document", json=parameters)
    
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data