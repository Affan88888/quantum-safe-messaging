// src/components/ChatSidebar.js

import React from 'react';
import './ChatSidebar.css';

const ChatSidebar = ({ chats, selectedChat, setSelectedChat, isDarkMode }) => {
  return (
    <div className={`chat-sidebar ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <div className="sidebar-header">
          <div className="title"><h3>Chats</h3></div>
      </div>
      <div className="chat-list">
        {chats.length > 0 ? (
          chats.map((chat) => (
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
          ))
        ) : (
          <div className="no-chats">No chats found.</div>
        )}
      </div>
    </div>
  );
};

export default ChatSidebar;