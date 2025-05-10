// src/pages/HomePage.js
import React from 'react';
import './HomePage.css'; // Import the CSS file

const HomePage = () => {
  return (

      <div>
        {/* navbar */}
        <nav className='navbar'>
          <div className="navbar-logo">QuantTalk</div>
          <div className='navbar-buttons'>
            <a href="/login" className="button login-button">Log In</a>
            <a href="/signup" className="button signup-button">Sign Up</a>
          </div>
        </nav>
        
        {/* novi hero section */}
        <div className="hero-section">
          <div className="container">
            <h1>Private messaging secured by post-quantum cryptography</h1>
            <p>
              Simple, reliable communication that's safe from quantum threats, available worldwide
            </p>
            <div className="hero-buttons">
              
              <a href="/signup" className="button get-started">Get Started</a>
              <a href="#features" className="button learn-more">Learn More</a>
            </div>
          </div>
          <div className="hero-phone">
            {/* Placeholder for app screenshot */}
            <div className="phone"></div>
          </div>
        </div>

        {/* Features Section */}
        <section className="features">
          <h2>Key features</h2>
          {/* napravit cemo kartice da ljepse izgleda */}
          <div className="features-grid">
            <div className="features-card">
              <div className="feature-icon">🔐</div>
              <h3>Quantum-Safe Encryption</h3>
              <p>End-to-end encryption using CRYSTALS-Kyber and CRYSTALS-Dilithium algorithms.</p>
            </div>
            <div className="features-card">
              <div className="feature-icon">⚡</div>
              <h3>Fast and reliable communication</h3>
              <p>nemam idejeeeee treba nesto napisati ovdjee</p>
            </div>
            <div className="features-card">
              <div className="feature-icon">🛡️</div>
              <h3>Future-Proof Security</h3>
              <p>Protection against both classical and quantum computing threats.</p>
            </div>
          </div>
        </section>
        
        {/* Technologies Section */}
        <section className="tech-section">
          <h2>Built With Cutting-Edge Technology</h2>
          <div className="tech-card">
            <div className="tech-item">
              <div className="tech-logo-react"></div>
              <span>React.js</span>
            </div>
            <div className="tech-item">
              <div className="tech-logo-flask"></div>
              <span>Flask</span>
            </div>
            <div className="tech-item">
              <div className="tech-logo-mysql"></div>
              <span>MySQL</span>
            </div>
            <div className="tech-item">
              <div className="tech-logo-openssl"></div>
              <span>OpenSSL 3.x</span>
            </div>
            <div className="tech-item">
              <div className="tech-logo-oqs"></div>
              <span>OQS Provider</span>
            </div>
          </div>
        </section>
      </div>
  );
};

export default HomePage;