from flask import Blueprint, request, jsonify, session
from models.messaging_model import create_chat
from utils.db import get_db_connection

messaging_bp = Blueprint('messaging', __name__)

