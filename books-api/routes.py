from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from db import get_books_collection

books_collection = get_books_collection()

def book_routes(app):
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
        if 'image' in request.files:
            image = request.files['image']
            # Here you would typically upload the image to a storage service
            # and store the URL in the database
            # For this example, we'll just store a placeholder
            book['image_url'] = 'placeholder_url'
        
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
        if 'image' in request.files:
            image = request.files['image']
            # Here you would typically upload the image to a storage service
            # and update the URL in the database
            update_data['image_url'] = 'placeholder_url'
        
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