from flask import request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from db import get_users_collection

users_collection = get_users_collection()

def register_routes(app):
    @app.route('/', methods=['GET'])
    def root():
        return "Flask is running!", 200
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password!'}), 400

        if users_collection.find_one({'username': data['username']}):
            return jsonify({'error': 'Username already exists!'}), 400

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = {
            'username': data['username'],
            'password': hashed_password
        }
        users_collection.insert_one(user)
        return jsonify({'message': 'User registered successfully'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password!'}), 400

        user = users_collection.find_one({'username': data['username']})
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            token = create_access_token(identity=str(user['_id']))
            return jsonify({'token': token}), 200

        return jsonify({'error': 'Invalid username or password'}), 401