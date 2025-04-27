// src/components/ContactSidebar.js
import React, { useState, useEffect } from 'react';
import './ContactSidebar.css';

const ContactSidebar = ({ onAddContact }) => {
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
        setErrorMessage('User with this email does not exist.');
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
  const handleChat = (contactId, contactName) => {
    console.log(`Chatting with contact: ${contactName} (ID: ${contactId})`);
    handleCloseContextMenu();
    // You can add logic here to navigate to a chat window or trigger a chat action
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
    <div className="contact-sidebar">
      <div className="sidebar-header">
        <h2>Contacts</h2>
        <button className="add-contact-button" onClick={openModal}>
          Add Contact
        </button>
      </div>
      <div className="contact-list">
        {contacts.length > 0 ? (
          contacts.map((contact) => (
            <div
              key={contact.id}
              className="contact-item"
              onContextMenu={(e) => handleRightClick(e, contact)} // Handle right-click
            >
              <div className="contact-avatar">{contact.username[0]}</div>
              <div className="contact-info">
                <div className="contact-name">{contact.username}</div>
                <div className="contact-email">{contact.email}</div>
              </div>
            </div>
          ))
        ) : (
          <div className="no-contacts">No contacts added yet.</div>
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
            />
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <div className="modal-buttons">
              <button className="cancel-button" onClick={closeModal}>
                Cancel
              </button>
              <button className="add-button" onClick={handleAddContact}>
                Add
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
            onClick={() => handleChat(contextMenu.contactId, contextMenu.contactName)}
          >
            Chat
          </button>
          <button
            className="context-menu-option"
            onClick={() => handleDelete(contextMenu.contactId, contextMenu.contactName)}
          >
            Delete
          </button>
        </div>
      )}

      {/* Close context menu when clicking outside */}
      {contextMenu && <div className="context-menu-overlay" onClick={handleCloseContextMenu}></div>}
    </div>
  );
};

export default ContactSidebar;