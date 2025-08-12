from flask import request, jsonify, url_for, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import os
from db import get_books_collection
from werkzeug.utils import secure_filename

books_collection = get_books_collection()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def book_routes(app):
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
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

        # Handle image upload
        if 'image' not in request.files:
            return jsonify({"message": "Không tìm thấy file"}), 400

        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            book['image_url'] = f"/books-api/uploads/{filename}"

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
        
        # Handle image upload
        if 'image' not in request.files:
            return jsonify({"message": "Không tìm thấy file"}), 400

        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            update_data['image_url'] = f"/books-api/uploads/{filename}"
        
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
        result = books_collection.delete_one({'_id': ObjectId(book_id), 'user_id': user_id})

        if result.deleted_count == 0:
            return jsonify({'error': 'Book not found'}), 404

        return jsonify({'message': 'Book deleted successfully'}), 200

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)