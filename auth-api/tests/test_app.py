import unittest
from unittest.mock import patch, MagicMock
from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("routes.users_collection")
    def test_register_success(self, mock_users):
        mock_users.find_one.return_value = None
        mock_users.insert_one.return_value = MagicMock()

        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.get_data(as_text=True))

    @patch("routes.users_collection")
    def test_register_duplicate_user(self, mock_users):
        mock_users.find_one.return_value = {"username": "testuser"}

        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "testpass"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username already exists", response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()