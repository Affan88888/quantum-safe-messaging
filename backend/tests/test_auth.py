import unittest
from app import app
from flask_testing import TestCase
import json
import uuid

class TestAuth(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_signup(self):
        unique_email = f'testuser_{uuid.uuid4()}@example.com'

        response = self.client.post('/api/auth/signup', json={
            'username': f'testuser_{uuid.uuid4().hex[:8]}',
            'email': unique_email,
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', json.loads(response.data))

    def test_login(self):
        # First register
        self.client.post('/api/auth/signup', json={
            'username': 'loginuser',
            'email': 'login@example.com',
            'password': 'password123'
        })

        # Now try login
        response = self.client.post('/api/auth/login', json={
            'email': 'login@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.data)['user'])

    def test_check_auth(self):
        # Test without login
        response = self.client.get('/api/auth/check-auth')
        self.assertEqual(json.loads(response.data)['authenticated'], False)

if __name__ == '__main__':
    unittest.main()
