// src/pages/HomePage.js
import React from 'react';
import './HomePage.css'; // Import the CSS file

const HomePage = () => {
  return (
    <div className="container">
      <h1>Welcome to QuantumSafe Messenger</h1>
      <p>Your secure, quantum-safe messaging platform.</p>
      <div className="features">
        <h2>Key Features:</h2>
        <ul>
          <li>End-to-end encryption using quantum-safe algorithms</li>
          <li>Fast and reliable communication</li>
          <li>User-friendly interface</li>
        </ul>
      </div>
      <div className="cta">
        <p>Ready to get started?</p>
        <a href="/login" className="button">Login</a>
        <a href="/signup" className="button">Sign Up</a>
      </div>
    </div>
  );
};

export default HomePage;