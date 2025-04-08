import React, { useState } from 'react';
import './ContactSidebar.css';

const ContactSidebar = ({ contacts, onAddContact }) => {
  const [newContactEmail, setNewContactEmail] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

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
      // Simulate an API call to validate the email
      const response = await fetch('http://localhost:5000/api/contact/check-email', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: newContactEmail }),
      });

      const data = await response.json();

      if (data.exists) {
        // Add the contact if the email exists
        onAddContact(newContactEmail);
        closeModal();
      } else {
        // Show an error message if the email does not exist
        setErrorMessage('User with this email does not exist.');
      }
    } catch (error) {
      console.error('Error checking email:', error);
      setErrorMessage('An error occurred while checking the email.');
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
            <div key={contact.id} className="contact-item">
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
    </div>
  );
};

export default ContactSidebar;