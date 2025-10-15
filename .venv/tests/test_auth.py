"""
Authentication tests for QuMail
"""

import pytest
from backend.app import create_app
from backend.models import db
from backend.models.user import User


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
def test_user(app):
    """Create test user."""
    with app.app_context():
        user = User(
            email='test@example.com',
            full_name='Test User'
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        return user


class TestAuthentication:
    """Test authentication functionality."""

    def test_register_success(self, client):
        """Test successful user registration."""
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'full_name': 'New User'
        }

        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 201
        assert 'User registered successfully' in response.get_json()['message']

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email."""
        data = {
            'email': 'test@example.com',  # Same as test_user
            'password': 'password123',
            'full_name': 'Another User'
        }

        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 409
        assert 'Email already registered' in response.get_json()['error']

    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        data = {
            'email': 'invalid-email',
            'password': 'password123',
            'full_name': 'Test User'
        }

        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        assert 'Invalid email format' in response.get_json()['error']

    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        data = {
            'email': 'test@example.com',
            'password': '123',  # Too short
            'full_name': 'Test User'
        }

        response = client.post('/api/auth/register', json=data)
        assert response.status_code == 400
        assert 'at least 8 characters' in response.get_json()['error']

    def test_login_success(self, client, test_user):
        """Test successful login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

        response = client.post('/api/auth/login', json=data)
        assert response.status_code == 200
        assert 'Login successful' in response.get_json()['message']
        assert 'user' in response.get_json()

    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }

        response = client.post('/api/auth/login', json=data)
        assert response.status_code == 401
        assert 'Invalid email or password' in response.get_json()['error']

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }

        response = client.post('/api/auth/login', json=data)
        assert response.status_code == 401
        assert 'Invalid email or password' in response.get_json()['error']

    def test_check_auth_unauthenticated(self, client):
        """Test auth check for unauthenticated user."""
        response = client.get('/api/auth/check')
        assert response.status_code == 200
        assert response.get_json()['authenticated'] is False

    def test_user_search(self, client, test_user):
        """Test user search functionality."""
        # Login first
        client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })

        # Search for existing user
        response = client.get('/api/auth/users/search?email=test@example.com')
        assert response.status_code == 200
        assert response.get_json()['found'] is True

        # Search for non-existent user
        response = client.get('/api/auth/users/search?email=notfound@example.com')
        assert response.status_code == 200
        assert response.get_json()['found'] is False