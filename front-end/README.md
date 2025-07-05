# Book Management System Frontend

This is the frontend application for the Book Management System, built with React 19 and Vite 6.

## Tech Stack

- React 19
- React Router DOM 5.2
- Axios 0.21.1
- Vite 6.3.5
- Testing Libraries:
  - @testing-library/react 16.3.0
  - @testing-library/jest-dom 6.6.3
  - @testing-library/user-event 13.5.0

## Development

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```
The application will be available at http://localhost:5173

3. Other available commands:
```bash
npm run dev-watch  # Run with host watching enabled
npm run build     # Build for production
npm run lint      # Run ESLint
npm run preview   # Preview production build
```

## Docker Development

The frontend can also be run through Docker using the provided Dockerfile.dev:

```bash
docker compose up frontend
```

This will start the frontend with hot-reload enabled at http://localhost:3000

## Project Structure

```
.
├── src/
│   ├── components/
│   │   ├── BookForm.jsx    # Book creation/editing form
│   │   ├── BookList.jsx    # List of books display
│   │   ├── Login.jsx       # Login form
│   │   ├── Register.jsx    # Registration form
│   │   └── PrivateRoute.jsx # Protected route wrapper
│   ├── context/
│   │   └── AuthContext.jsx  # Authentication context
│   └── App.jsx             # Main application component
├── index.html
├── package.json
├── vite.config.js
└── eslint.config.js
```

## Features

- User authentication (login/register)
- Protected routes
- Book management:
  - View all books
  - Add new books
  - Edit existing books
  - Delete books
- Responsive design
- Hot Module Replacement (HMR)
- ESLint configuration for code quality