from app import app
from app import app, users_collection
from flask import Flask
from flask import Flask, jsonify
from flask import json
from flask.testing import FlaskClient
from pymongo import MongoClient
from unittest.mock import patch, MagicMock
import json
import pytest

class TestApp:

    def test_login_invalid_credentials(self, client):
        """
        Test the login endpoint with invalid credentials.
        This test verifies that the login function correctly handles
        the case when the provided username and password are invalid.
        """
        response = client.post('/login', json={
            'username': 'nonexistent_user',
            'password': 'wrong_password'
        })
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['error'] == 'Invalid username or password'

    def test_login_missing_credentials(self, client):
        """
        Test the login endpoint with missing credentials.
        This test verifies that the login function correctly handles
        the case when username or password is missing from the request data.
        """
        response = client.post('/login', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing username or password!'

    def test_login_missing_credentials_2(self):
        """
        Test login functionality when username or password is missing.

        This test verifies that the login endpoint returns an appropriate error
        message and status code when the request is missing either the username
        or password.

        Expected behavior:
        - Response status code should be 400
        - Response body should contain an error message about missing credentials
        """
        client = app.test_client()

        # Test with missing username
        response = client.post('/login', json={'password': 'testpassword'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing username or password!'

        # Test with missing password
        response = client.post('/login', json={'username': 'testuser'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing username or password!'

        # Test with empty request body
        response = client.post('/login', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing username or password!'

    def test_register_3(self):
        """
        Test successful user registration when username and password are provided and username does not exist.

        This test verifies that:
        1. The register endpoint accepts valid registration data.
        2. A new user is successfully added to the database.
        3. The response contains a success message and 201 status code.
        """
        # Setup
        client = app.test_client()
        users_collection.delete_many({})  # Clear the collection before test

        # Test data
        test_user = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        # Execute
        response = client.post('/register', json=test_user)

        # Assert
        assert response.status_code == 201
        assert json.loads(response.data) == {'message': 'User registered successfully'}

        # Verify user was added to the database
        user_in_db = users_collection.find_one({'username': 'testuser'})
        assert user_in_db is not None
        assert 'password' in user_in_db  # Password should be hashed and stored

    def test_register_existing_username(self):
        """
        Test registration with an existing username.
        This tests the explicit check for existing username in the register function.
        """
        client = app.test_client()
        with patch.object(users_collection, 'find_one', return_value={'username': 'existinguser'}):
            response = client.post('/register', json={'username': 'existinguser', 'password': 'test123'})
            assert response.status_code == 400
            assert response.get_json() == {'error': 'Username already exists hehe!'}

    def test_register_missing_credentials(self):
        """
        Testcase 1 for def register():
        Tests the scenario where username or password is missing in the request data.
        Expected behavior: Returns a 400 error with a specific error message.
        """
        client = app.test_client()
        response = client.post('/register', json={})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Missing username or password hehe!'}

    def test_register_missing_data(self):
        """
        Test registration with missing data in the request.
        This tests the explicit check for missing username or password in the register function.
        """
        client = app.test_client()
        response = client.post('/register', json={})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Missing username or password hehe!'}

    def test_register_missing_password(self):
        """
        Test registration with missing password in the request.
        This tests the explicit check for missing password in the register function.
        """
        client = app.test_client()
        response = client.post('/register', json={'username': 'testuser'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Missing username or password hehe!'}

    def test_register_missing_username(self):
        """
        Test registration with missing username in the request.
        This tests the explicit check for missing username in the register function.
        """
        client = app.test_client()
        response = client.post('/register', json={'password': 'test123'})
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Missing username or password hehe!'}

    def test_register_username_already_exists(self):
        """
        Tests the register function when the username already exists in the database.

        Scenario:
        - Valid username and password are provided
        - The username already exists in the database

        Expected outcome:
        - Returns a JSON response with an error message
        - HTTP status code 400
        """
        with app.test_client() as client:
            with patch.object(users_collection, 'find_one', return_value=True):
                response = client.post('/register', json={
                    'username': 'existing_user',
                    'password': 'password123'
                })

                assert response.status_code == 400
                assert response.get_json() == {'error': 'Username already exists hehe!'}

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
