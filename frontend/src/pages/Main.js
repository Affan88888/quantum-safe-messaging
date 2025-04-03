// src/pages/Main.js
import React from 'react';
import { useUser } from '../services/UserContext';
import './Main.css';

const Main = () => {
  const { user, logout } = useUser(); // Get the user state and logout function from the context

  // Function to handle logout
  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/auth/logout', {
        method: 'POST',
        credentials: 'include', // Include cookies for session management
      });
      if (response.ok) {
        logout(); // Call the logout function from the context
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  return (
    <div className="main-container">
      <h1>{user ? `Welcome ${user.username} to Your Dashboard` : 'Loading...'}</h1>
      <div className="main-actions">
        <button className="action-button">Message Users</button>
        <button className="action-button">Create Group Chat</button>
        <button className="action-button">View Recent Messages</button>
      </div>
      {/* Add the Logout button */}
      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
};

export default Main;