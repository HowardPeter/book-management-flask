import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import BookList from './components/BookList';
import BookForm from './components/BookForm';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Switch>
            <Route exact path="/login" component={Login} />
            <Route exact path="/register" component={Register} />
            <PrivateRoute exact path="/books" component={BookList} />
            <PrivateRoute exact path="/books/new" component={BookForm} />
            <PrivateRoute exact path="/books/edit/:id" component={BookForm} />
            <Redirect from="/" to="/books" />
          </Switch>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;