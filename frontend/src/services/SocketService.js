import io from 'socket.io-client';

// Initialize the WebSocket connection globally
const socket = io('http://localhost:5000', {
  withCredentials: true, // Include cookies/sessions for authentication
});

export default socket;