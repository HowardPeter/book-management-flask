import unittest
import json
from app import app
from db import users_collection

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.test_user = {
            "username": "testuser",
            "password": "testpassword"
        }
        # Xóa trước nếu tồn tại (tránh trùng user khi chạy nhiều lần)
        users_collection.delete_many({'username': self.test_user['username']})

    def tearDown(self):
        users_collection.delete_many({'username': self.test_user['username']})

    def test_register_success(self):    
        response = self.client.post('/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))

    def test_register_duplicate_username(self):
        # Đăng ký lần đầu
        self.client.post('/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        # Đăng ký lần 2 với cùng username
        response = self.client.post('/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', response.get_data(as_text=True))

    def test_login_success(self):
        # Đảm bảo user tồn tại
        self.client.post('/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        # Login
        response = self.client.post('/login',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/login',
            data=json.dumps({
                "username": "nonexistent",
                "password": "wrongpass"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
