import React, { useState } from 'react';
import { useUser } from '../services/UserContext';
import { useNavigate } from 'react-router-dom';
import ChatSidebar from '../components/ChatSidebar';
import ContactSidebar from '../components/ContactSidebar';
import './Main.css';

const Main = () => {
  const { user, logout } = useUser();
  const navigate = useNavigate();

  // Mock data for chats
  const [chats, setChats] = useState([
    { id: 1, name: 'Alice', lastMessage: 'Hey there!', timestamp: '10:30 AM' },
    { id: 2, name: 'Bob', lastMessage: 'Are we meeting today?', timestamp: '9:45 AM' },
    { id: 3, name: 'Group Chat', lastMessage: 'John: See you at 5!', timestamp: 'Yesterday' },
  ]);

  // Mock data for contacts
  const [contacts, setContacts] = useState([]);

  // State to track the currently selected chat
  const [selectedChat, setSelectedChat] = useState(null);

  // State to toggle between "Chats" and "Contacts"
  const [isChatSidebar, setIsChatSidebar] = useState(true);

  // Function to handle adding a new contact
  const handleAddContact = (email) => {
    const newContact = { id: contacts.length + 1, username: email.split('@')[0], email };
    setContacts([...contacts, newContact]);
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
          <ContactSidebar contacts={contacts} onAddContact={handleAddContact} />
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