# app.py

from flask import Flask, session
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_session import Session  # 👈 New import for server-side sessions
from routes.auth_routes import auth_bp
from routes.contact_routes import contact_bp
from routes.chats_routes import chat_bp
from routes.messaging_routes import messaging_bp, socketio  # Import messaging routes and SocketIO
from config import SECRET_KEY
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])  # Allow frontend origin

# 🔐 Secret key for session management
app.secret_key = SECRET_KEY

# 📁 Create session storage directory if not exists
SESSION_FOLDER = os.path.join(os.getcwd(), 'flask_sessions')
os.makedirs(SESSION_FOLDER, exist_ok=True)

# 🔧 Session configuration for server-side storage
app.config.update({
    'SESSION_TYPE': 'filesystem',              # Use local filesystem to store session data
    'SESSION_FILE_DIR': SESSION_FOLDER,        # Folder for session files
    'SESSION_FILE_THRESHOLD': 500,             # Max number of session files
    'SESSION_DEFAULT_COOKIE_NAME': 'session',  # Default cookie name
    'SESSION_PERMANENT': True,                 # Keep session alive across restarts
    'SESSION_USE_SIGNER': True,                # Sign session cookie for better security
    'SESSION_COOKIE_SECURE': False,            # Set to True in production with HTTPS
    'SESSION_COOKIE_HTTPONLY': True,           # Prevent JS access
    'SESSION_COOKIE_SAMESITE': 'Lax',          # Protect against CSRF
})

# 🛠️ Initialize Flask-Session
Session(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(chat_bp, url_prefix='/api/chats')
app.register_blueprint(messaging_bp, url_prefix='/api/messaging')  # Register messaging blueprint

# Initialize SocketIO with the app
socketio.init_app(app, cors_allowed_origins="http://localhost:3000")  # Allow frontend origin for WebSocket

if __name__ == '__main__':
    print(f"Session files stored at: {SESSION_FOLDER}")
    socketio.run(app, host='0.0.0.0', port=5000)