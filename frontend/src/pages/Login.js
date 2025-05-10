// src/pages/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Hook for navigation
import { useUser } from '../services/UserContext'; // Import the useUser hook
import './Login.css'; // Import the CSS file for styling
import '@fortawesome/fontawesome-free/css/all.min.css';

const Login = () => {
  // State to manage form inputs
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // Initialize the navigation hook
  const { login } = useUser(); // Get the login function from the context

  // Handler for form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send a POST request to the Flask backend's /login route
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        credentials: 'include', // Include cookies in the request
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      // Parse the response as JSON
      const data = await response.json();

      if (response.ok) {
        // Call the login function to update the context with the user data
        login(data.user);

        // If login is successful, redirect to the /main page
        navigate('/main');
      } else {
        // Display an error message if login fails
        alert(data.error || 'Login failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An unexpected error occurred. Please try again.');
    }
  };

  return (
    //dodao novi glavni div da mogu staviti background
    <div className='background'>
      <div className="login-container">
        <h1>Login</h1>
        <p>Please enter your credentials to log in.</p>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
        <p className="signup-link">
          Don't have an account? <a href="/signup">Sign up here</a>.
        </p>
        <button className="home-button" onClick={() => navigate('/')}>
          <i className="fas fa-arrow-left"></i>Back to Home Page
        </button>
      </div>
    </div>
  );
};

export default Login;