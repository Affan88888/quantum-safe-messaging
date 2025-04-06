import React, { useState } from 'react';
import { useUser } from '../services/UserContext';
import { useNavigate } from 'react-router-dom';
import './Main.css';

const Main = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  // Mock data for chats (replace this with real data fetched from your backend)
  const [chats, setChats] = useState([
    { id: 1, name: 'Alice', lastMessage: 'Hey there!', timestamp: '10:30 AM' },
    { id: 2, name: 'Bob', lastMessage: 'Are we meeting today?', timestamp: '9:45 AM' },
    { id: 3, name: 'Group Chat', lastMessage: 'John: See you at 5!', timestamp: 'Yesterday' },
  ]);

  // State to track the currently selected chat
  const [selectedChat, setSelectedChat] = useState(null);

  // Function to handle logout
  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        logout();
        navigate('/');
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  return (
    <div className="main-container">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Chats</h2>
          <button className="new-chat-button">New Chat</button>
        </div>
        <div className="chat-list">
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${selectedChat?.id === chat.id ? 'selected' : ''}`}
              onClick={() => setSelectedChat(chat)}
            >
              <div className="chat-avatar">{chat.name[0]}</div>
              <div className="chat-info">
                <div className="chat-name">{chat.name}</div>
                <div className="last-message">{chat.lastMessage}</div>
              </div>
              <div className="timestamp">{chat.timestamp}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {selectedChat ? (
          <>
            <div className="chat-header">
              <div className="chat-avatar">{selectedChat.name[0]}</div>
              <div className="chat-name">{selectedChat.name}</div>
            </div>
            <div className="message-list">
              {/* Mock messages for the selected chat */}
              <div className="message received">
                <div className="message-content">Hello!</div>
                <div className="timestamp">10:25 AM</div>
              </div>
              <div className="message sent">
                <div className="message-content">Hi, how are you?</div>
                <div className="timestamp">10:30 AM</div>
              </div>
            </div>
            <div className="message-input">
              <input type="text" placeholder="Type a message..." />
              <button className="send-button">Send</button>
            </div>
          </>
        ) : (
          <div className="no-chat-selected">
            <h3>Select a chat to start messaging</h3>
          </div>
        )}
      </div>

      {/* Logout Button */}
      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
};

export default Main;