import json
import pytest
from flask import Flask
from app import app as flask_app
from app import users_collection
from unittest.mock import patch, MagicMock
import bcrypt
from bson import ObjectId

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_register_success(client):
    with patch.object(users_collection, 'find_one', return_value=None), \
         patch.object(users_collection, 'insert_one', return_value=MagicMock()):
        payload = {"username": "testuser", "password": "testpass"}
        response = client.post("/register", json=payload)
        assert response.status_code == 201
        assert response.get_json() == {"message": "User registered successfully"}

def test_register_missing_data(client):
    response = client.post("/register", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing username or password hehe!"}

def test_register_existing_user(client):
    with patch.object(users_collection, 'find_one', return_value={"username": "testuser"}):
        payload = {"username": "testuser", "password": "testpass"}
        response = client.post("/register", json=payload)
        assert response.status_code == 400
        assert response.get_json() == {"error": "Username already exists hehe!"}

def test_login_success(client):
    password = "secret123"
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    mock_user = {
        "_id": ObjectId(),
        "username": "testuser",
        "password": hashed
    }

    with patch.object(users_collection, 'find_one', return_value=mock_user):
        response = client.post("/login", json={
            "username": "testuser",
            "password": password
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "token" in data

def test_login_wrong_password(client):
    real_password = "secret123"
    wrong_password = "wrongpass"
    hashed = bcrypt.hashpw(real_password.encode("utf-8"), bcrypt.gensalt())

    mock_user = {
        "_id": ObjectId(),
        "username": "testuser",
        "password": hashed
    }

    with patch.object(users_collection, 'find_one', return_value=mock_user):
        response = client.post("/login", json={
            "username": "testuser",
            "password": wrong_password
        })
        assert response.status_code == 401
        assert response.get_json() == {"error": "Invalid username or password"}

def test_login_nonexistent_user(client):
    with patch.object(users_collection, 'find_one', return_value=None):
        response = client.post("/login", json={
            "username": "nouser",
            "password": "nopass"
        })
        assert response.status_code == 401
        assert response.get_json() == {"error": "Invalid username or password"}

def test_login_missing_data(client):
    response = client.post("/login", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing username or password!"}
