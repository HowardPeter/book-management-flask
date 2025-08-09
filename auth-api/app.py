from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from routes import register_routes
from db import check_connection

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

register_routes(app)

if __name__ == '__main__':
    check_connection()
    app.run(host='0.0.0.0', port=5000, debug=True)