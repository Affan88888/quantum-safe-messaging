# app.py

from flask import Flask, session
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from config import SECRET_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask backend is running!"

# Secret key for session management
app.secret_key = SECRET_KEY

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)