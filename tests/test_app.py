from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query():
    response = client.post('/api/query', json={'query': 'deep learning'})
    assert response.status_code == 200
