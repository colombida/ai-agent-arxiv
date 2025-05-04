from fastapi import FastAPI
from .routes import router
from .database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api")

# tests/test_app.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_populate_then_query():
    # First populate a few entries
    resp1 = client.post('/api/populate?max_results=3')
    assert resp1.status_code == 200
    # Then query
    resp2 = client.post('/api/query', json={'query': 'quantum'})
    assert resp2.status_code == 200
    data = resp2.json()
    assert 'results' in data