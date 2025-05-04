// src/components/Chat.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000', {
  withCredentials: true,
});

const Chat = ({ selectedChat, user }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  // Fetch chat history when the selected chat changes
  useEffect(() => {
    if (!selectedChat) return;

    const fetchChatHistory = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/messaging/get-chat-history`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ chat_id: selectedChat.id }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch chat history');
        }

        const data = await response.json();
        setMessages(data.chat_history || []);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };

    fetchChatHistory();

    // Cleanup function to remove listeners
    return () => {
      socket.off('receive_message');
    };
  }, [selectedChat]);

  // Set up WebSocket listener for new messages
  useEffect(() => {
    if (!selectedChat) return;

    socket.on('receive_message', (message) => {
      if (message.chat_id === selectedChat.id) {
        setMessages((prevMessages) => [...prevMessages, message]);
      }
    });

    return () => {
      socket.off('receive_message');
    };
  }, [selectedChat]);

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedChat) return;

    try {
      const messageData = {
        chat_id: selectedChat.id,
        sender_id: user.id,
        content: newMessage,
      };

      // Send the message via WebSocket
      socket.emit('send_message', messageData);

      // Optimistically update the UI
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          sender_id: user.id,
          sender_username: user.username,
          content: newMessage,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);

      // Clear the input field
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="chat-container">
      {/* Chat Header */}
      <div className="chat-header">
        <div className="chat-avatar">{selectedChat.name[0]}</div>
        <div className="chat-name">{selectedChat.name}</div>
      </div>

      {/* Message List */}
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender_id === user.id ? 'sent' : 'received'}`}>
            <div className="message-content">{msg.content}</div>
            <div className="timestamp">{msg.timestamp}</div>
          </div>
        ))}
      </div>

      {/* Message Input */}
      <div className="message-input">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button className="send-button" onClick={handleSendMessage}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;