// src/components/ChatSidebar.js
import React from 'react';
import './ChatSidebar.css';

// Helper function to format the timestamp
const formatTimestamp = (timestamp) => {
  const now = new Date(); // Current date and time
  const messageDate = new Date(timestamp); // Parse the timestamp

  // Calculate the difference in milliseconds between now and the message date
  const diffTime = now - messageDate;
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24)); // Difference in days

  // If the message is from today, show the time in 12-hour format
  if (diffDays === 0) {
    const hours = messageDate.getHours();
    const minutes = messageDate.getMinutes();
    const period = hours >= 12 ? 'PM' : 'AM';
    const formattedHours = hours % 12 || 12; // Convert 0 to 12 for 12-hour format
    const formattedMinutes = String(minutes).padStart(2, '0');
    return `${formattedHours}:${formattedMinutes} ${period}`;
  }

  // If the message is from yesterday, show "Yesterday"
  if (diffDays === 1) {
    return 'Yesterday';
  }

  // If the message is from 2 to 7 days ago, show the day of the week
  if (diffDays > 1 && diffDays <= 7) {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return daysOfWeek[messageDate.getDay()];
  }

  // If the message is more than 7 days ago, show the date in day/month/year format
  const day = messageDate.getDate();
  const month = messageDate.getMonth() + 1; // Months are zero-indexed
  const year = messageDate.getFullYear();
  return `${day}/${month}/${year}`;
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