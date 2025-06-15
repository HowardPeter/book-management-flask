import unittest
from app import app, books_collection
from flask_jwt_extended import create_access_token
from bson import ObjectId

class BooksApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.user_id = "testuser123"
        self.token = create_access_token(identity=self.user_id)
        self.headers = {"Authorization": f"Bearer {self.token}"}

        # Clean up test data before run
        books_collection.delete_many({'user_id': self.user_id})

    def test_create_book(self):
        response = self.app.post('/books', headers=self.headers, data={
            'name': 'Test Book',
            'author': 'Test Author',
            'publish_year': '2024'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.get_json())

    def test_create_book_without_name(self):
        # Thiếu 'name' trong dữ liệu
        response = self.app.post('/books', headers=self.headers, data={
            'author': 'No Name Author',
            'publish_year': '2024'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        
    def test_get_books(self):
        books_collection.insert_one({
            'name': 'Temp Book',
            'author': 'Author',
            'publish_year': '2023',
            'user_id': self.user_id
        })

        response = self.app.get('/books', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_book(self):
        inserted = books_collection.insert_one({
            'name': 'Old Name',
            'author': 'Author',
            'publish_year': '2020',
            'user_id': self.user_id
        })

        response = self.app.put(f"/books/{inserted.inserted_id}", headers=self.headers, data={
            'name': 'Updated Name'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())
    def test_update_nonexistent_book(self):
        fake_id = str(ObjectId())  # Tạo ID không tồn tại
        response = self.app.put(f"/books/{fake_id}", headers=self.headers, data={
            'name': 'Ghost Book'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_delete_book(self):
        inserted = books_collection.insert_one({
            'name': 'To Be Deleted',
            'author': 'Author',
            'publish_year': '2022',
            'user_id': self.user_id
        })

        response = self.app.delete(f"/books/{inserted.inserted_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_delete_nonexistent_book(self):
        fake_id = str(ObjectId())
        response = self.app.delete(f"/books/{fake_id}", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_unauthorized_access(self):
        # Không gửi Authorization header
        response = self.app.get('/books')  # GET là đại diện, áp dụng cho mọi route có @jwt_required
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', response.get_json())

    def tearDown(self):
        books_collection.delete_many({'user_id': self.user_id})

if __name__ == '__main__':
    unittest.main()
