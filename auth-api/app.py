from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Import và đăng ký routes
from routes import register_routes
register_routes(app)

# Chỉ check kết nối khi chạy thực tế, không kiểm tra khi import để test
if __name__ == '__main__':
    from db import check_connection
    check_connection()
    app.run(host='0.0.0.0', port=5000, debug=True)