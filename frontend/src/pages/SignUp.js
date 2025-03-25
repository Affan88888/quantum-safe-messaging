// src/pages/SignUp.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Hook for navigation
import './SignUp.css'; // Import the CSS file for styling

const SignUp = () => {
  // State to manage form inputs
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate(); // Initialize the navigation hook

  // Handler for form submission
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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      // Parse the response as JSON
      const data = await response.json();

      if (response.ok) {
        // If signup is successful, redirect to the /main page
        alert(data.message || 'User registered successfully');
        navigate('/main'); // Redirect to the main page
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
    </div>
  );
};

export default SignUp;