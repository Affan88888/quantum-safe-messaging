// src/pages/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Hook for navigation
import './Login.css'; // Import the CSS file for styling

const Login = () => {
  // State to manage form inputs
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // Initialize the navigation hook

  // Handler for form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    // Simulate authentication (replace with actual API call to Flask backend)
    if (email === 'user@example.com' && password === 'password') {
      // Redirect to the Main page on successful login
      navigate('/main');
    } else {
      alert('Invalid email or password');
    }

    // Log the credentials for debugging purposes
    console.log('Logging in with:', { email, password });
  };

  return (
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
    </div>
  );
};

export default Login;