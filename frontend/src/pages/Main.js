// src/pages/Main.js
import React, { useState, useEffect } from 'react';
import { useUser } from '../services/UserContext';
import { useNavigate } from 'react-router-dom';
import ChatSidebar from '../components/ChatSidebar';
import ContactSidebar from '../components/ContactSidebar';
import Chat from '../components/Chat'; // Import the Chat component
import './Main.css';

const Main = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  // State for chats
  const [chats, setChats] = useState([]);
  // State for contacts
  const [contacts, setContacts] = useState([]);
  // State to track the currently selected chat
  const [selectedChat, setSelectedChat] = useState(null);
  // State to toggle between "Chats" and "Contacts"
  const [isChatSidebar, setIsChatSidebar] = useState(true);
  // State for dark mode
  const [isDarkMode, setIsDarkMode] = useState(false);
  // State to control the visibility of the settings menu
  const [isSettingsMenuOpen, setIsSettingsMenuOpen] = useState(false);

  // Apply the user's theme preference on mount
  useEffect(() => {
    if (user?.theme === 'dark') {
      setIsDarkMode(true);
    } else {
      setIsDarkMode(false);
    }
  }, [user]);

  // Function to update the user's theme preference in the backend
  const updateThemePreference = async (newTheme) => {
    try {
      const response = await fetch('http://localhost:5000/api/theme/update-theme', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ theme: newTheme }),
      });

      if (!response.ok) {
        throw new Error('Failed to update theme');
      }

      const data = await response.json();
      console.log(data.message); // Log success message
    } catch (error) {
      console.error('Error updating theme preference:', error);
    }
  };

  // Function to toggle dark mode
  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);

    // Update the theme preference in the backend
    updateThemePreference(newMode ? 'dark' : 'light');
  };

  // Function to fetch chats from the backend
  const fetchChats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/chats/get-chat-list', {
        method: 'GET',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch chats');
      }

      const data = await response.json();
      setChats(data.chats || []);
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
    const existingChat = chats.find((chat) => chat.name === contact.username);
    if (existingChat) {
      setSelectedChat(existingChat);
    } else {
      const newChat = {
        id: chats.length + 1,
        name: contact.username,
        lastMessage: '',
        timestamp: 'Now',
      };
      setChats([...chats, newChat]);
      setSelectedChat(newChat);
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
    <div className={`main-container ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      {/* Sidebar */}
      <div className="sidebar">
        <h1>{user ? `Welcome ${user.username}!` : 'Loading...'}</h1>

        {/* Toggle Buttons */}
        <div className="toggle-buttons">
          <button
            className={`toggle-button ${isChatSidebar ? 'active' : ''}`}
            onClick={() => setIsChatSidebar(true)}
          >
            <h3>Chats</h3>
          </button>
          <button
            className={`toggle-button ${!isChatSidebar ? 'active' : ''}`}
            onClick={() => setIsChatSidebar(false)}
          >
            <h3>Contacts</h3>
          </button>
        </div>

        {/* Conditional Rendering of Sidebars */}
        {isChatSidebar ? (
          <ChatSidebar
            chats={chats}
            selectedChat={selectedChat}
            setSelectedChat={setSelectedChat}
            isDarkMode={isDarkMode}
          />
        ) : (
          <ContactSidebar
            contacts={contacts}
            onAddContact={handleAddContact}
            onStartChat={handleStartChat}
            isDarkMode={isDarkMode}
          />
        )}

        {/* Settings Button */}
        <div className="settings-button-container">
          {/* Settings Button */}
          <button className="settings-button">
            {/* Icon with onClick handler */}
            <span
              className="icon"
              onClick={() => setIsSettingsMenuOpen((prev) => !prev)}
            >
              ⚙️
            </span>
            {/* Text shown on hover */}
            <span className="settings-text">Settings</span>
          </button>

          {/* Settings Menu */}
          {isSettingsMenuOpen && (
            <div className="settings-menu">
              {/* Close Button */}
              <button
                className="close-button"
                onClick={() => setIsSettingsMenuOpen(false)}
              >
                &times; {/* Unicode for "X" symbol */}
              </button>

              {/* Dark Mode Toggle Button */}
              <button className="dark-mode-toggle" onClick={toggleDarkMode}>
                {isDarkMode ? (
                  <>
                    <span className="icon">☀️</span><h5>Light Mode</h5>
                  </>
                ) : (
                  <>
                    <span className="icon">🌙</span><h5>Dark Mode</h5>
                  </>
                )}
              </button>

              {/* Logout Button */}
              <button className="logout-button" onClick={handleLogout}>
                <i className="fas fa-right-from-bracket icon"></i> <h5>Logout</h5>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {selectedChat ? (
          <Chat selectedChat={selectedChat} user={user} />
        ) : (
          <div className="no-chat-selected">
            <h3>Select a chat to start messaging</h3>
          </div>
        )}
      </div>
    </div>
  );
};

export default Main;