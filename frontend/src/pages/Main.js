// src/pages/Main.js
import React from 'react';
import { useUser } from '../services/UserContext';
import './Main.css';

const Main = () => {
  const { user } = useUser(); // Get the user state from the context

  return (
    <div className="main-container">
      <h1>{user ? `Welcome ${user.username} to Your Dashboard` : 'Loading...'}</h1>
      <div className="main-actions">
        <button className="action-button">Message Users</button>
        <button className="action-button">Create Group Chat</button>
        <button className="action-button">View Recent Messages</button>
      </div>
    </div>
  );
};

export default Main;