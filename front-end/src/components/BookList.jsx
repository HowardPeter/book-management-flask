import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function BookList() {
  const [books, setBooks] = useState([]);
  const { token, logout } = useAuth();
  const history = useHistory();

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await axios.get('/books-api/books', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
      if (error.response?.status === 401) {
        logout();
        history.push('/login');
      }
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this book?')) {
      try {
        await axios.delete(`/books-api/books/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchBooks();
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    }
  };

  return (
    <div>
      <h2>My Books</h2>
      <Link to="/books/new">Add New Book</Link>
      <button onClick={() => {
        logout();
        history.push('/login');
      }}>Logout</button>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Author</th>
            <th>Publish Year</th>
            <th>Image</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book) => (
            <tr key={book._id}>
              <td>{book.name}</td>
              <td>{book.author}</td>
              <td>{book.publish_year}</td>
              <td>
                {book.image_url && (
                  <img
                    src={book.image_url}
                    alt={book.name}
                    style={{ width: '50px', height: '50px' }}
                  />
                )}
              </td>
              <td>
                <Link to={`/books/edit/${book._id}`}>Edit</Link>
                <button onClick={() => handleDelete(book._id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BookList;