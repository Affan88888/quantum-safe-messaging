// src/pages/HomePage.js
import React from 'react';
import './HomePage.css'; // Import the CSS file
// ovdje importovati jos jednu sliku
import latticeImage from './background_picture/lattice-based-cryptography-image.png'; // import photos for learn more
import ckImage from './background_picture/crystals-kyber-image.png';
import liboqsLibrary from './background_picture/liboqs_library.png'

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
              <a href="#learn-more" className="button learn-more">Learn More</a>
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

        {/* learn more link button from hero section */}
        <section id='learn-more' className='learn-more'>
          {/* Section 1 */}
          <div className='learn-more-section'>
            <div className='learn-more-text'>
              <h2>Open Quantum Safe (OQS) Project</h2>
              <p>
                The Open Quantum Safe (OQS) project is an open-source initiative aimed at supporting the development and integration of quantum-resistant cryptographic algorithms. It provides tools like liboqs, a C library for quantum-safe algorithms, and integrations with protocols such as OpenSSL. OQS plays a crucial role in transitioning to cryptographic standards that can withstand quantum computing threats.
              </p>
            </div>
            <div className='learn-more-image'>
              <img src={liboqsLibrary} alt='Open Quantum Safe Project' />
            </div>
          </div>

          {/* Section 2 */}
          <div className='learn-more-section reverse'>
            
            <div className='learn-more-text'>
              <h2>Lattice-Based Cryptography</h2>
              <p>
                Lattice-based cryptography relies on complex mathematical structures called lattices, which are grids of points in multidimensional space. The security of these cryptographic schemes is based on the difficulty of solving certain problems within these lattices, a challenge even for quantum computers. This makes lattice-based cryptography a strong candidate for post-quantum security.
              </p>
            </div>
            <div className='learn-more-image'>
              <img src={latticeImage} alt='Lattice-Based Cryptography' />
            </div>
          </div>

          {/* Section 3 */}
          <div className='learn-more-section'>
            <div className='learn-more-text'>
              <h2>CRYSTALS-Kyber and CRYSTALS-Dilithium Algorithms</h2>
              <p>
                CRYSTALS-Kyber and CRYSTALS-Dilithium are cryptographic algorithms designed to be secure against quantum attacks. Kyber is used for key encapsulation, while Dilithium is used for digital signatures. Both algorithms have been selected by NIST for standardization, highlighting their robustness and efficiency in post-quantum cryptographic applications.
              </p>
            </div>
            <div className='learn-more-image'>
              <img src={ckImage} alt='CRYSTALS-Kyber and Dilithium' />
            </div>
          </div>
        </section>
      </div>
  );
};

export default HomePage;