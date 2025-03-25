# app.py

from flask import Flask, session
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from config import SECRET_KEY

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])  # Explicitly allow your frontend origin

# Secret key for session management
app.secret_key = SECRET_KEY

# Secure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = False  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF attacks

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)