from flask import request, jsonify, url_for, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import os
from db import get_books_collection
from werkzeug.utils import secure_filename
import uuid

books_collection = get_books_collection()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEFAULT_IMAGE = "empty.jpg"

def book_routes(app):
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def save_uploaded_image(file_storage, upload_folder):
        if file_storage and allowed_file(file_storage.filename):
            filename = secure_filename(file_storage.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            save_path = os.path.join(upload_folder, unique_filename)
            file_storage.save(save_path)
            return unique_filename
        return None
    
    @app.route('/', methods=['GET'])
    def root():
        return "Flask is running!", 200

    @app.route('/books', methods=['POST'])
    @jwt_required()
    def create_book():
        data = request.form.to_dict()
        
        if not data.get('name'):
            return jsonify({'error': 'Book name is mandatory'}), 400
        
        book = {
            'name': data['name'],
            'author': data.get('author', ''),
            'publish_year': data.get('publish_year', ''),
            'user_id': get_jwt_identity()
        }

        image_file = request.files.get('image')
        filename = save_uploaded_image(image_file, app.config['UPLOAD_FOLDER'])

        if filename:
            book['image_url'] = f"/books-api/uploads/{filename}"
        else:
            book['image_url'] = f"/books-api/uploads/{DEFAULT_IMAGE}"

        result = books_collection.insert_one(book)
        book['_id'] = str(result.inserted_id)
        return jsonify(book), 201

    @app.route('/books', methods=['GET'])
    @jwt_required()
    def get_books():
        user_id = get_jwt_identity()
        books = list(books_collection.find({'user_id': user_id}))
        
        # Convert ObjectId to string for JSON serialization
        for book in books:
            book['_id'] = str(book['_id'])
        
        return jsonify(books), 200

    @app.route('/books/<book_id>', methods=['GET'])
    @jwt_required()
    def get_book(book_id):
        user_id = get_jwt_identity()
        book = books_collection.find_one({'_id': ObjectId(book_id), 'user_id': user_id})
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        book['_id'] = str(book['_id'])
        return jsonify(book), 200

    @app.route('/books/<book_id>', methods=['PUT'])
    @jwt_required()
    def update_book(book_id):
        user_id = get_jwt_identity()
        data = request.form.to_dict()
        
        if not data.get('name'):
            return jsonify({'error': 'Book name is mandatory'}), 400
        
        update_data = {
            'name': data['name'],
            'author': data.get('author', ''),
            'publish_year': data.get('publish_year', '')
        }
        
        image_file = request.files.get('image')
        filename = save_uploaded_image(image_file, app.config['UPLOAD_FOLDER'])

        if filename:
            update_data['image_url'] = f"/update_datas-api/uploads/{filename}"
        else:
            update_data['image_url'] = f"/books-api/uploads/{DEFAULT_IMAGE}"
        
        result = books_collection.update_one(
            {'_id': ObjectId(book_id), 'user_id': user_id},
            {'$set': update_data}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Book not found'}), 404

        return jsonify({'message': 'Book updated successfully'}), 200

    @app.route('/books/<book_id>', methods=['DELETE'])
    @jwt_required()
    def delete_book(book_id):
        user_id = get_jwt_identity()
        deleted_book = books_collection.find_one({'_id': ObjectId(book_id), 'user_id': user_id})
        result = books_collection.delete_one(deleted_book)
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Book not found'}), 404
        
        # Remove the image file if it exists
        if 'image_url' in deleted_book and deleted_book['image_url'] != f"/books-api/uploads/{DEFAULT_IMAGE}":
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], deleted_book['image_url'].split('/')[-1])
            if os.path.exists(image_path):
                os.remove(image_path)

        return jsonify({'message': 'Book deleted successfully'}), 200

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)