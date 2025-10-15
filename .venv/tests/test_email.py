"""
Email functionality tests for QuMail
"""

import pytest
import json
from backend.app import create_app
from backend.models import db
from backend.models.user import User
from backend.models.email import Email


@pytest.fixture
def app():
    """Create test app fixture."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def test_users(app):
    """Create test users."""
    with app.app_context():
        sender = User(email='sender@example.com', full_name='Sender User')
        sender.set_password('password123')

        recipient = User(email='recipient@example.com', full_name='Recipient User')
        recipient.set_password('password123')

        db.session.add(sender)
        db.session.add(recipient)
        db.session.commit()

        return sender, recipient


@pytest.fixture
def authenticated_client(client, test_users):
    """Create authenticated client."""
    sender, _ = test_users
    client.post('/api/auth/login', json={
        'email': sender.email,
        'password': 'password123'
    })
    return client, sender


class TestEmail:
    """Test email functionality."""

    def test_send_email_success(self, authenticated_client, test_users):
        """Test successful email sending."""
        client, sender = authenticated_client
        _, recipient = test_users

        data = {
            'recipient_email': recipient.email,
            'subject': 'Test Email',
            'body': 'This is a test email.',
            'security_level': 4  # Standard encryption for testing
        }

        response = client.post('/api/email/send', json=data)
        assert response.status_code == 201
        assert response.get_json()['success'] is True

    def test_send_email_invalid_recipient(self, authenticated_client):
        """Test sending email to invalid recipient."""
        client, _ = authenticated_client

        data = {
            'recipient_email': 'nonexistent@example.com',
            'subject': 'Test Email',
            'body': 'This is a test email.',
            'security_level': 4
        }

        response = client.post('/api/email/send', json=data)
        assert response.status_code == 400
        assert 'Recipient not found' in response.get_json()['error']

    def test_send_email_invalid_security_level(self, authenticated_client, test_users):
        """Test sending email with invalid security level."""
        client, _ = authenticated_client
        _, recipient = test_users

        data = {
            'recipient_email': recipient.email,
            'subject': 'Test Email',
            'body': 'This is a test email.',
            'security_level': 5  # Invalid level
        }

        response = client.post('/api/email/send', json=data)
        assert response.status_code == 400
        assert 'Invalid security level' in response.get_json()['error']

    def test_get_inbox(self, authenticated_client):
        """Test getting inbox emails."""
        client, _ = authenticated_client

        response = client.get('/api/email/inbox')
        assert response.status_code == 200
        assert 'emails' in response.get_json()

    def test_get_outbox(self, authenticated_client):
        """Test getting outbox emails."""
        client, _ = authenticated_client

        response = client.get('/api/email/outbox')
        assert response.status_code == 200
        assert 'emails' in response.get_json()