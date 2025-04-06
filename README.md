# Quantum-Safe Messaging App

A quantum-safe web application for secure messaging, leveraging post-quantum cryptographic algorithms to ensure future-proof security.

## Features
- Quantum-Safe Encryption : End-to-end encryption using quantum-safe algorithms (e.g., CRYSTALS-Kyber for key exchange and CRYSTALS-Dilithium for digital signatures).
- Message Encryption : Messages are encrypted using quantum-safe algorithms before being stored or transmitted.
- Session Encryption : Sessions are encrypted using quantum-safe algorithms to ensure secure communication between the client and server.
- Scalable Architecture : Reverse proxying via HAProxy and hosting on a Python Flask server for secure and efficient traffic handling.
- Database Integration : Secure storage of user data and messages in a MySQL database.

## Technologies
- Frontend : React.js
- Backend : Flask (Python)
- Database : MySQL
- Quantum-Safe Cryptography : OpenSSL 3.x with Open Quantum Safe (OQS) provider
- Web Servers :
    - HAProxy: For SSL termination and load balancing.
- Post-Quantum Algorithms : CRYSTALS-Kyber (Key Encapsulation Mechanism) and CRYSTALS-Dilithium (Digital Signature Algorithm).

## Installation
1. Follow these tutorials to install quantum-safe OpenSSL and other dependencies:
    - [Quantum-Safe OpenSSL Tutorial](https://developer.ibm.com/tutorials/awb-quantum-safe-openssl/)
    - [Building Quantum-Safe Web Applications](https://developer.ibm.com/tutorials/awb-building-quantum-safe-web-applications/)
2. Clone the repository: `git clone https://github.com/Affan88888/quantum-safe-messaging.git`
3. Install backend dependencies: `pip install -r backend/requirements.txt`
4. Clone the liboqs-python repository and install it manually.
5. Install frontend dependencies: `cd frontend && npm install`
6. Create a `.env` file in \backend directory, based off of `.env.example` file.
7. Build HAProxy with quantum-safe OpenSSL, copy the server certificates to the certs directory, and configure HAProxy to forward traffic to the Flask backend. Start HAProxy after completing the configuration.
8. Set up the MySQL database and ensure the backend application can connect to it. Update the database connection settings in the backend configuration if needed. Then run `python mySQL.py` in \backend.
9. Start the development server: `npm start` in \frontend and `python app.py` in \backend.
