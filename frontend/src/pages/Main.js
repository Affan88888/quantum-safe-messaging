import React from 'react';
import './Main.css'; // Import the CSS file for styling

const Main = () => {
  return (
    <div className="main-container">
      <h1>Welcome to Your Dashboard</h1>
      <div className="main-actions">
        <button className="action-button">Message Users</button>
        <button className="action-button">Create Group Chat</button>
        <button className="action-button">View Recent Messages</button>
      </div>
    </div>
  );
};

export default Main;