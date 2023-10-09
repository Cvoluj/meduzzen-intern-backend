import pytest
from httpx import AsyncClient
from app.main import app
import asyncio

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Create a user using your API
        user_data = {
            "user_email": "emailthatnotindb333@example.com",
            "user_firstname": "NameThatNotInDb333",
            "hashed_password": "hashedpass"
        }
        response = await client.post("/user/", json=user_data)
        
        assert response.status_code == 200
        

        assert response.json() == {"result": f"User {user_data['user_firstname']} created successfully"}


@pytest.mark.asyncio
async def test_get_user_by_id():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        user_id = 1  
        response = await client.get(f"/user/{user_id}")
        assert response.status_code == 200
