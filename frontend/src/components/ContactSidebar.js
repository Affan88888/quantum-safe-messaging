import React from 'react';
import './ContactSidebar.css';

const ContactSidebar = ({ contacts, onAddContact }) => {
  const [newContactEmail, setNewContactEmail] = React.useState('');

  const handleAddContact = () => {
    if (newContactEmail.trim()) {
      onAddContact(newContactEmail);
      setNewContactEmail('');
    }
  };

  
  return (
    <div className="contact-sidebar">
      <div className="sidebar-header">
        <h2>Contacts</h2>
        <button className="add-contact-button" onClick={handleAddContact}>
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
      <div className="add-contact-input">
        <input
          type="email"
          value={newContactEmail}
          onChange={(e) => setNewContactEmail(e.target.value)}
          placeholder="Enter contact email"
        />
        <button className="add-button" onClick={handleAddContact}>
          Add
        </button>
      </div>
    </div>
  );
};

export default ContactSidebar;