// src/pages/SignUp.js
import React, { useState } from 'react';
import { useUser } from '../services/UserContext';
import { useNavigate } from 'react-router-dom'; // Import the navigation hook
import socket from '../services/SocketService'; // Import the centralized socket
import './SignUp.css'; // Import the CSS file for styling

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { login } = useUser(); // Get the login function from the context
  const navigate = useNavigate(); // Initialize the navigation hook

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if passwords match
    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    try {
      // Send a POST request to the Flask backend's /signup route
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Automatically log the user in
        login(data.user);

        // Explicitly connect the WebSocket after successful sign-up
        socket.connect();

        // Redirect to the main page
        navigate('/main');

        // Show a success message
        alert(data.message || 'User registered successfully');
      } else {
        // Display an error message if signup fails
        alert(data.error || 'An error occurred during sign-up.');
      }
    } catch (error) {
      console.error('Error during sign-up:', error);
      alert('An unexpected error occurred. Please try again.');
    }
  };

  return (
    //dodao novi glavni div da mogu staviti background
    <div className='background'>
      <div className="signup-container">
        <h1>Sign Up</h1>
        <p>Please enter your details to create an account.</p>
        <form onSubmit={handleSubmit} className="signup-form">
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
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
          <div className="form-group">
            <label htmlFor="confirm-password">Confirm Password:</label>
            <input
              type="password"
              id="confirm-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="signup-button">
            Sign Up
          </button>
        </form>
        <p className="login-link">
          Already have an account? <a href="/login">Log in here</a>.
        </p>
        <button className="home-button" onClick={() => navigate('/')}>
          <i className="fas fa-arrow-left"></i>Back to Home Page
        </button>
      </div>
    </div>
  );
};

export default SignUp;