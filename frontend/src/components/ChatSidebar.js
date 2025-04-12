// src/components/ChatSidebar.js
import React from 'react';
import './ChatSidebar.css';

const ChatSidebar = ({ chats, selectedChat, setSelectedChat }) => {
  return (
    <div className="chat-sidebar">
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
  );
};

export default ChatSidebar;