// src/components/Chat.js

import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './Chat.css';

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

      // Ensure the message belongs to the currently selected chat
      if (message.chat_id === selectedChat.id) {
        setMessages((prevMessages) => {
          // Ensure the `id` is a string
          const receivedMessage = { ...message, id: String(message.id) };

          // Check if the message is an optimistic update (temporary ID)
          const isOptimistic = prevMessages.some(
            (msg) => typeof msg.id === 'string' && msg.id.startsWith('temp-') && msg.content === receivedMessage.content
          );

          if (isOptimistic) {
            // Replace the optimistic message with the final message
            return prevMessages.map((msg) =>
              typeof msg.id === 'string' && msg.id.startsWith('temp-') && msg.content === receivedMessage.content
                ? { ...receivedMessage, sender_id: user.id } // Ensure sender_id matches user.id
                : msg
            );
          }

          // Add the message only if it's from the recipient (not the current user)
          if (message.sender_id !== user.id) {
            // Add the new message if it's not a duplicate
            const isDuplicate = prevMessages.some((msg) => msg.id === receivedMessage.id);
            if (!isDuplicate) {
              return [...prevMessages, receivedMessage];
            }
          }

          // Return the unchanged state if the message is a duplicate or from the current user
          return prevMessages;
        });
      }
    });

    // Cleanup WebSocket listeners on unmount
    return () => {
      socket.off('receive_message');
    };
  }, [selectedChat, user]);

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedChat) return;

    try {
      const tempMessageId = `temp-${Date.now()}`; // Temporary unique ID for optimistic update

      const messageData = {
        chat_id: selectedChat.id,
        sender_id: user.id,
        content: newMessage,
      };

      // Optimistically update the UI with a temporary message
      const optimisticMessage = {
        id: tempMessageId, // Temporary ID for optimistic update
        sender_id: user.id,
        sender_username: user.username,
        content: newMessage,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prevMessages) => [...prevMessages, optimisticMessage]);

      // Send the message via WebSocket
      socket.emit('send_message', messageData);

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
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender_id === user.id ? 'sent' : 'received'}`}>
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