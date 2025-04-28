// src/pages/Main.js

import React, { useState, useEffect } from 'react'; // Import useEffect for fetching data
import { useUser } from '../services/UserContext';
import { useNavigate } from 'react-router-dom';
import ChatSidebar from '../components/ChatSidebar';
import ContactSidebar from '../components/ContactSidebar';
import './Main.css';

const Main = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  // State for chats (initialize as an empty array)
  const [chats, setChats] = useState([]);

  // Mock data for contacts (can also be replaced with a database call later)
  const [contacts, setContacts] = useState([]);

  // State to track the currently selected chat
  const [selectedChat, setSelectedChat] = useState(null);

  // State to toggle between "Chats" and "Contacts"
  const [isChatSidebar, setIsChatSidebar] = useState(true);

  // Function to fetch chats from the backend
  const fetchChats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/chats/get-chat-list', {
        method: 'GET',
        credentials: 'include', // Include cookies/sessions for authentication
      });

      if (!response.ok) {
        throw new Error('Failed to fetch chats');
      }

      const data = await response.json();
      setChats(data.chats || []); // Update the chats state with the fetched data
    } catch (error) {
      console.error('Error fetching chats:', error);
    }
  };

  // Fetch chats when the component mounts
  useEffect(() => {
    fetchChats();
  }, []);

  // Function to handle adding a new contact
  const handleAddContact = (email) => {
    const newContact = { id: contacts.length + 1, username: email.split('@')[0], email };
    setContacts([...contacts, newContact]);
  };

  // Function to start a chat with a contact
  const handleStartChat = (contact) => {
    // Check if a chat with the contact already exists
    const existingChat = chats.find((chat) => chat.name === contact.username);
    if (existingChat) {
      setSelectedChat(existingChat); // Select the existing chat
    } else {
      // Create a new chat for the contact
      const newChat = {
        id: chats.length + 1,
        name: contact.username,
        lastMessage: '',
        timestamp: 'Now',
      };
      setChats([...chats, newChat]); // Add the new chat to the list
      setSelectedChat(newChat); // Set the new chat as the selected chat
    }
  };

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
        {/* Welcome Message */}
        <h1>{user ? `Welcome ${user.username}!` : 'Loading...'}</h1>

        {/* Toggle Buttons */}
        <div className="toggle-buttons">
          <button
            className={`toggle-button ${isChatSidebar ? 'active' : ''}`}
            onClick={() => setIsChatSidebar(true)}
          >
            Chats
          </button>
          <button
            className={`toggle-button ${!isChatSidebar ? 'active' : ''}`}
            onClick={() => setIsChatSidebar(false)}
          >
            Contacts
          </button>
        </div>

        {/* Conditional Rendering of Sidebars */}
        {isChatSidebar ? (
          <ChatSidebar chats={chats} selectedChat={selectedChat} setSelectedChat={setSelectedChat} />
        ) : (
          <ContactSidebar
            contacts={contacts}
            onAddContact={handleAddContact}
            onStartChat={handleStartChat} // Pass the function to start a chat
          />
        )}
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