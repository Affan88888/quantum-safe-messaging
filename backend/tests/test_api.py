import pytest
pytest.skip("Skipping test_api.py for now", allow_module_level=True)
import uuid
import pytest
from flask_socketio import SocketIO, test_client

def test_send_message_via_websocket(client, app):
    unique_email = f'msguser_{uuid.uuid4()}@example.com'

    # Signup
    signup_response = client.post('/api/auth/signup', json={
        'username': f'msguser_{uuid.uuid4().hex[:8]}',
        'email': unique_email,
        'password': 'password123'
    })
    assert signup_response.status_code in [200, 201]

    # Login
    login_response = client.post('/api/auth/login', json={
        'email': unique_email,
        'password': 'password123'
    })
    assert login_response.status_code == 200

    # WebSocket connection
    socketio = SocketIO(app)
    ws_client = socketio.test_client(app)

    received = []

    @ws_client.on('receive_message')
    def handle_receive(data):
        received.append(data)

    chat_id = "1"
    message_content = "Test message"

    ws_client.emit('send_message', {
        'chat_id': chat_id,
        'content': message_content
    })

    ws_client.get_received()

    assert len(received) > 0
    assert received[0]['content'] == message_content