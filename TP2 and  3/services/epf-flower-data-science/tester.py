from google.cloud import firestore
import os

class FirestoreClient:
    """Wrapper around a Firestore database."""

    def __init__(self) -> None:
        """Initialize the Firestore client with credentials."""
        # Change 'path/to/your/credentials.json' to the path where your JSON key is stored
        credentials_path = 'epf-flower-credentials.json'
        self.client = firestore.Client.from_service_account_json(credentials_path)

    def test_connection(self):
        """Test the connection to Firestore."""
        try:
            # Test connection by retrieving the list of collections
            collections = self.client.collections()
            print("Connexion à Firestore réussie.")
            print("Liste des collections :")
            for collection in collections:
                print(collection.id)
        except Exception as e:
            print(f"Erreur de connexion à Firestore : {e}")

if __name__ == "__main__":
    firestore_client = FirestoreClient()
    firestore_client.test_connection()