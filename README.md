# Book Management System

This is a microservices-based web application for managing book information. The application consists of three main components:
- Authentication Service (auth-api)
- Books Service (books-api)
- React Frontend (front-end)

## Project Structure
```
.
├── auth-api/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── books-api/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── env/
│   ├── auth.env
│   └── books.env
├── front-end/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── components/
│       │   ├── BookForm.js
│       │   ├── BookList.js
│       │   ├── Login.js
│       │   ├── PrivateRoute.js
│       │   └── Register.js
│       ├── context/
│       │   └── AuthContext.js
│       └── App.js
└── docker-compose.yml
```

## Setup and Installation

The project uses Docker Compose for easy setup and deployment. Make sure you have Docker and Docker Compose installed on your system.

1. Configure environment variables:
   - Copy the example environment files and adjust as needed:
     ```bash
     # In the env directory
     cp auth.env.example auth.env
     cp books.env.example books.env
     ```

2. Build and start all services:
   ```bash
   docker compose up --build
   ```

This will start:
- MongoDB database
- Authentication service on http://localhost:5000
- Books service on http://localhost:5001
- Frontend application on http://localhost:3000

### Alternative Setup (Development)

If you prefer to run services individually:

#### Backend Services (auth-api and books-api)

1. Set up Python virtual environments for each service:
```bash
# For auth-api
cd auth-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# For books-api
cd ../books-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Start the services:
```bash
# In auth-api directory
python app.py  # Runs on port 5000

# In books-api directory
python app.py  # Runs on port 5001
```

#### Frontend

1. Install dependencies:
```bash
cd front-end
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173 when running in development mode.

## Features

- User authentication (signup/login)
- CRUD operations for books
- Book information includes:
  - Name (mandatory)
  - Author
  - Publish year
  - Image upload capability
- Protected routes requiring authentication
- MongoDB Atlas database integration

## API Endpoints

### Auth Service (http://localhost:5000)
- POST /register - Register new user
- POST /login - User login

### Books Service (http://localhost:5001)
- GET /books - Get all books for authenticated user
- POST /books - Create new book
- GET /books/:id - Get specific book
- PUT /books/:id - Update book
- DELETE /books/:id - Delete book

## Security Notes

- JWT is used for authentication
- Passwords are hashed using bcrypt
- All book operations require authentication
- Each user can only access their own books
- Services run in isolated Docker containers
- MongoDB credentials are managed through environment variables
- Environment files (.env) should never be committed to version control
- Frontend communicates with backend services through Docker network
- Volume mounts are used for development hot-reloading while maintaining container isolation

## Environment Variables

### Auth Service (auth.env)
Required variables:
- `MONGODB_URI`: MongoDB connection string
- `JWT_SECRET`: Secret key for JWT token generation
- `PORT`: Service port (default: 5000)

### Books Service (books.env)
Required variables:
- `MONGODB_URI`: MongoDB connection string
- `AUTH_SERVICE_URL`: URL of the auth service
- `PORT`: Service port (default: 5001)

### MongoDB
Default credentials (customize in docker-compose.yml):
- Username: admin
- Password: secret123

Note: For production deployment, ensure all passwords and secrets are changed from their default values.