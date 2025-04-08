// src/pages/HomePage.js
import React from "react";
import Image from "./Unknown.png";
import Logo from "./logo.png";
import "./HomePage.css";


export const WelcomePage = () => {
  return (
    <div className="welcome-page">
      <div className="overlap-wrapper">
        <div className="overlap">
          <div className="rectangle" />

          <div className="div" />

          <img
            className="vecteezy"
            alt="Vecteezy"
            src={Image}
          />
          

    

          <div className="rectangle-2" />
          <img className="image" alt="logo" src={Logo} />

          <div className="button">
            <div className="overlap-group">
              <div className="text-wrapper">Sign in</div>

            </div>
          </div>

          <div className="overlap-group-wrapper">
            <div className="overlap-group">
              <div className="text-wrapper-2">Log in</div>

            </div>
          </div>

          <p className="welcome-to-quanttalk">
            <span className="span">Welcome to Quan</span>

            <span className="text-wrapper-3">tt</span>

            <span className="span">alk Messenger</span>
          </p>

          <p className="endtoend-encryption">
            End-to-end encryption using quantum-safe algorithms
            <br />
            <br />
            Fast and reliable communication
            <br />
            <br />
            User-friendly interface
          </p>

          <p className="your-secure">
            Your Secure, Quantum-Safe Messaging Platform.
          </p>

          <div className="get-started">Get Started!</div>
        </div>
      </div>
    </div>
  );
};



export default WelcomePage;