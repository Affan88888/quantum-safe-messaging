// src/component/ContactSidebar.js

import React, { useState, useEffect } from 'react';
import './ContactSidebar.css';

const ContactSidebar = ({ onAddContact, onStartChat, isDarkMode }) => {
  const [newContactEmail, setNewContactEmail] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [contacts, setContacts] = useState([]); // State to hold the list of contacts
  const [contextMenu, setContextMenu] = useState(null); // State to manage the context menu

  // Fetch contacts when the component mounts
  useEffect(() => {
    const fetchContacts = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/contact/get-contact-list', {
          method: 'GET',
          credentials: 'include', // Include cookies/sessions for authentication
        });

        if (!response.ok) {
          throw new Error('Failed to fetch contacts');
        }

        const data = await response.json();
        setContacts(data.contacts || []); // Update the contacts state with the fetched data
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    };

    fetchContacts();
  }, []); // Empty dependency array ensures this runs only once on mount

  // Function to handle opening the modal
  const openModal = () => {
    setIsModalOpen(true);
    setErrorMessage('');
  };

  // Function to handle closing the modal
  const closeModal = () => {
    setIsModalOpen(false);
    setNewContactEmail('');
    setErrorMessage('');
  };

  // Function to handle adding a contact
  const handleAddContact = async () => {
    if (!newContactEmail.trim()) {
      setErrorMessage('Please enter a valid email.');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/contact/check-email', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: newContactEmail }),
      });

      const data = await response.json();

      if (data.exists) {
        const updatedResponse = await fetch('http://localhost:5000/api/contact/get-contact-list', {
          method: 'GET',
          credentials: 'include',
        });

        if (updatedResponse.ok) {
          const updatedData = await updatedResponse.json();
          setContacts(updatedData.contacts || []); // Update the contacts state with the new list
        }

        closeModal();
      } else {
        setErrorMessage(data.message);
      }
    } catch (error) {
      console.error('Error checking email:', error);
      setErrorMessage('An error occurred while checking the email.');
    }
  };

  // Function to handle right-click on a contact
  const handleRightClick = (event, contact) => {
    event.preventDefault(); // Prevent the default browser context menu
    setContextMenu({
      mouseX: event.clientX + 2,
      mouseY: event.clientY - 6,
      contactId: contact.id,
      contactName: contact.username,
    });
  };

  // Function to close the context menu
  const handleCloseContextMenu = () => {
    setContextMenu(null);
  };

// Function to handle chat with a contact
const handleChat = async (contactId, contactName) => {
  try {
    // Call the backend API to create a chat
    const response = await fetch('http://localhost:5000/api/chats/create-chat', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contact_id: contactId }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to create chat.');
    }

    const contact = contacts.find((c) => c.id === contactId);
    if (contact) {
      // Add the chat ID returned by the backend to the contact object
      contact.chatId = data.chatId;

      // Call the onStartChat function passed as a prop
      onStartChat(contact);

      // Refresh the page to reflect the new chat
      window.location.reload();
    }
  } catch (error) {
    console.error('Error creating chat:', error);
    setErrorMessage('An error occurred while starting the chat.');
  } finally {
    handleCloseContextMenu();
  }
};

  // Function to handle deleting a contact
  const handleDelete = async (contactId, contactName) => {
    if (window.confirm(`Are you sure you want to delete ${contactName}?`)) {
      try {
        const response = await fetch('http://localhost:5000/api/contact/delete-contact', {
          method: 'DELETE',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ contact_id: contactId }),
        });

        const data = await response.json();

        if (response.ok) {
          // Remove the deleted contact from the state
          setContacts((prevContacts) => prevContacts.filter((c) => c.id !== contactId));
          handleCloseContextMenu();
        } else {
          console.error('Error deleting contact:', data.error);
          setErrorMessage(data.error || 'An error occurred while deleting the contact.');
        }
      } catch (error) {
        console.error('Error deleting contact:', error);
        setErrorMessage('An error occurred while deleting the contact.');
      }
    }
  };

  return (
    <div className={`contact-sidebar ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      {/* Sidebar Header */}
      <div className="sidebar-header">
        <div className="title"><h3>Contacts</h3></div>
        <button className="add-contact-button" onClick={openModal}>
          <h5>Add Contact</h5>
        </button>
      </div>

      {/* Contact List */}
      <div className="contact-list">
        {contacts.length > 0 ? (
          contacts.map((contact) => (
            <div
              key={contact.id}
              className="contact-item"
              onContextMenu={(e) => handleRightClick(e, contact)}
            >
              <div className="contact-avatar">{contact.username[0]}</div>
              <div className="contact-info">
                <div className="contact-name">{contact.username}</div>
                <div className="contact-email">{contact.email}</div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-contacts"><h5>No contacts added yet.</h5></div>
        )}
      </div>

      {/* Modal for Adding a Contact */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Add New Contact</h3>
            <input
              type="email"
              value={newContactEmail}
              onChange={(e) => setNewContactEmail(e.target.value)}
              placeholder="Enter contact email"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleAddContact(); // Trigger the "Add" action on Enter key press
                }
              }}
            />
            {errorMessage && <h5 className="error-message">{errorMessage}</h5>}
            <div className="modal-buttons">
              <button className="cancel-button" onClick={closeModal}>
                <h5>Cancel</h5>
              </button>
              <button className="add-button" onClick={handleAddContact}>
                <h5>Add</h5>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Context Menu */}
      {contextMenu && (
        <div
          className="context-menu"
          style={{
            top: `${contextMenu.mouseY}px`,
            left: `${contextMenu.mouseX}px`,
          }}
        >
          <button
            className="context-menu-option"
            onClick={() =>
              handleChat(contextMenu.contactId, contextMenu.contactName)
            }
          >
            <h5>Chat</h5>
          </button>
          <button
            className="context-menu-option"
            onClick={() =>
              handleDelete(contextMenu.contactId, contextMenu.contactName)
            }
          >
            <h5>Delete</h5>
          </button>
        </div>
      )}

      {/* Close context menu when clicking outside */}
      {contextMenu && (
        <div className="context-menu-overlay" onClick={handleCloseContextMenu}></div>
      )}
    </div>
  );
};

export default ContactSidebar;