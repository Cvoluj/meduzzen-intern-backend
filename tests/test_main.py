from app.main import app
from app.routers.health import health_check
from fastapi.testclient import TestClient


client =  TestClient(app)

def test_health_check():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'status_code': 200,
        'detail': 'ok',
        'result': 'working'
    }