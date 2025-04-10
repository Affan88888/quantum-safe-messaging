// src/pages/HomePage.js
import React from 'react';
import './HomePage.css'; // Import the CSS file

const HomePage = () => {
  return (
      <div className="container">
        <header className="hero">
          <h1>QuantumSafe Messenger</h1>
          <p>Your secure, quantum-safe messaging platform.</p>
        </header>

        <section className="features">
          <h2>Key Features:</h2>
          <ul>
            <li><span className="icon">🔒</span> End-to-end encryption using quantum-safe algorithms</li>
            <li><span className="icon">⚡</span> Fast and reliable communication</li>
            <li><span className="icon">📱</span> User-friendly interface</li>
          </ul>
        </section>

        <section className="cta">
          <p>Ready to get started?</p>
          <div className="buttons">
            <a href="/login" className="button login-button">Login</a>
            <a href="/signup" className="button signup-button">Sign Up</a>
          </div>
        </section>
      </div>
  );
};

export default HomePage;