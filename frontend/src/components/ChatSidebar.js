// src/components/ChatSidebar.js
import React from 'react';
import './ChatSidebar.css';

// Helper function to format the timestamp
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp); // Parse the timestamp
  const hours = date.getHours(); // Get the hour (0-23)
  const minutes = date.getMinutes(); // Get the minutes (0-59)

  // Determine AM or PM
  const period = hours >= 12 ? 'PM' : 'AM';

  // Convert to 12-hour format
  const formattedHours = hours % 12 || 12; // Convert 0 to 12 for 12-hour format

  // Ensure minutes are always two digits
  const formattedMinutes = String(minutes).padStart(2, '0');

  // Return the formatted time as a string
  return `${formattedHours}:${formattedMinutes} ${period}`;
};

const ChatSidebar = ({ chats, selectedChat, setSelectedChat, isDarkMode }) => {
  return (
    <div className={`chat-sidebar ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="sidebar-header">
        <div className="title"><h3>Chats</h3></div>
      </div>
      <div className="chat-list">
        {chats.length > 0 ? (
          chats.map((chat) => {
            // Format the timestamp before rendering
            const formattedTime = formatTimestamp(chat.timestamp);

            return (
              <div
                key={chat.id}
                className={`chat-item ${selectedChat?.id === chat.id ? 'selected' : ''}`}
                onClick={() => setSelectedChat(chat)}
              >
                <div className="chat-avatar">{chat.name[0]}</div>
                <div className="chat-info">
                  <div className="chat-name">{chat.name}</div>
                  <div className="last-message">{chat.last_message}</div>
                </div>
                <div className="timestamp">{formattedTime}</div>
              </div>
            );
          })
        ) : (
          <div className="no-chats"><h5>No chats found.</h5></div>
        )}
      </div>
    </div>
  );
};

export default ChatSidebar;