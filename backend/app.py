# app.py

from flask import Flask, session
from flask_cors import CORS
from flask_socketio import SocketIO
from routes.auth_routes import auth_bp
from routes.contact_routes import contact_bp
from routes.chats_routes import chat_bp
from routes.messaging_routes import messaging_bp, socketio
from routes.user_theme_routes import theme_bp
from config import SECRET_KEY

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])  # Allow frontend origin

# Secret key for session management
app.secret_key = SECRET_KEY

# Secure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = False  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF attacks

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(chat_bp, url_prefix='/api/chats')
app.register_blueprint(messaging_bp, url_prefix='/api/messaging')
app.register_blueprint(theme_bp, url_prefix = '/api/theme')

# Initialize SocketIO with the app
socketio.init_app(app, cors_allowed_origins="http://localhost:3000")  # Allow frontend origin for WebSocket

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)  # Run the app with WebSocket support