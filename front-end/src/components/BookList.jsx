import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './BookList.css';
import './Body.css'

function BookList() {
  const [books, setBooks] = useState([]);
  const { token, logout } = useAuth();
  const history = useHistory();

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      // const response = await axios.get('/books-api/books', {
      //   headers: { Authorization: `Bearer ${token}` }
      // });
      const response = await axios.get('http://localhost:5001/books', {
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
        // await axios.delete(`/books-api/books/${id}`, {
        //   headers: { Authorization: `Bearer ${token}` }
        // });
        await axios.delete(`http://localhost:5001/books/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchBooks();
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    }
  };

  return (
    <div className="book-list-container">
      <div className="book-list-header">
        <h2>Store your books</h2>
        <div className='button-header'>
          <button className="add-book-btn" onClick={() => history.push('/books/new')}>
            Add book
          </button>
          <button className="logout-btn" onClick={() => history.push('/login')}>
            Logout
          </button>
        </div>
      </div>
      <div className="book-table-scroll">
        <table className="book-table">
          <thead>
            <tr>
              <th>Book Cover</th>
              <th>Book Name</th>
              <th>Author</th>
              <th>Publish Year</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {books.map((book) => (
              <tr key={book._id}>
                <td>
                  {book.image_url ? (
                    <img
                      src={book.image_url}
                      alt={book.name}
                      className="book-cover"
                    />
                  ) : (
                    <div className="book-cover">📕</div>
                  )}
                </td>
                <td>{book.name}</td>
                <td>{book.author}</td>
                <td>{book.publish_year}</td>
                <td>
                  <div className="action-buttons">
                    <button
                      className="edit-btn"
                      onClick={() => history.push(`/books/edit/${book._id}`)}
                    >
                      Edit
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(book._id)}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default BookList;