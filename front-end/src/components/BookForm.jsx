import React, { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './BookForm.css';
import './Body.css'

function BookForm() {
  const { id } = useParams();
  const history = useHistory();
  const { token } = useAuth();
  const [book, setBook] = useState({
    name: '',
    author: '',
    publish_year: '',
  });
  const [image, setImage] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      fetchBook();
    }
  }, [id]);

  const fetchBook = async () => {
    try {
      const response = await axios.get(`/books/books/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBook(response.data);
    } catch (error) {
      console.error('Error fetching book:', error);
      setError('Error fetching book details');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', book.name);
    formData.append('author', book.author);
    formData.append('publish_year', book.publish_year);
    if (image) {
      formData.append('image', image);
    }

    try {
      if (id) {
        await axios.put(`/books-api/books/${id}`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          }
        });
      } else {
        await axios.post('/books-api/books', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          }
        });
      }
      history.push('/books');
    } catch (error) {
      console.error('Error saving book:', error);
      setError(error.response?.data?.error || 'Error saving book');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBook(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  return (
    <div className="book-form-container">
      <h2>{id ? 'Edit Book' : 'Add New Book'}</h2>
      {error && <p className="error-message">{error}</p>}
      <form className="book-form" onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            name="name"
            value={book.name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Author:</label>
          <input
            type="text"
            name="author"
            value={book.author}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Publish Year:</label>
          <input
            type="text"
            name="publish_year"
            value={book.publish_year}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Image:</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>
        <div className="book-form-buttons">
          <button type="submit" className="save-btn">Save</button>
          <button
            type="button"
            className="cancel-btn"
            onClick={() => history.push('/books')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default BookForm;