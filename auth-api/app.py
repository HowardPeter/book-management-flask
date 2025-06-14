from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import bcrypt
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# MongoDB connection using Docker-compatible URI
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_DB = os.environ.get("MONGODB_DB")

mongo_uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@mongodb:27017/{MONGODB_DB}?authSource=admin"
client = MongoClient(mongo_uri)

try:
    # Thử kết nối với MongoDB server
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully.")
except ConnectionFailure as e:
    print("❌ Failed to connect to MongoDB:", e)
    # Optionally: exit the app if connection fails
    import sys
    sys.exit(1)

db = client[MONGODB_DB]
users_collection = db.users

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password hehe!'}), 400
    
    if users_collection.find_one({'username': data['username']}):
        return jsonify({'error': 'Username already exists hehe!'}), 400
    
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
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({'token': access_token}), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)