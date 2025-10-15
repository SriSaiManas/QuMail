"""
Quantum service tests for QuMail
"""

import pytest
from backend.app import create_app
from backend.models import db
from backend.models.user import User
from backend.services.quantum_service import QuantumService
from backend.services.encryption_service import EncryptionService


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
        user = User(email='test@example.com', full_name='Test User')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user


class TestQuantumService:
    """Test quantum service functionality."""

    def test_encryption_service_init(self):
        """Test encryption service initialization."""
        service = EncryptionService()
        assert service is not None

    def test_level_4_encryption_decryption(self):
        """Test standard encryption/decryption (Level 4)."""
        service = EncryptionService()
        test_data = "This is a test message for encryption."

        # Encrypt
        encrypted = service.encrypt_data(test_data, 4)
        assert encrypted['security_level'] == 4
        assert encrypted['algorithm'] == 'STANDARD'
        assert 'encrypted_data' in encrypted

        # Decrypt
        decrypted = service.decrypt_data(encrypted)
        assert decrypted == test_data

    def test_level_2_encryption_with_quantum_key(self):
        """Test quantum-aided AES encryption (Level 2)."""
        service = EncryptionService()
        test_data = "This is a test message for QKD-AES encryption."
        quantum_key = b'a' * 32  # 32-byte key for AES

        # Encrypt
        encrypted = service.encrypt_data(test_data, 2, quantum_key)
        assert encrypted['security_level'] == 2
        assert encrypted['algorithm'] == 'AES-QKD'

        # Decrypt
        decrypted = service.decrypt_data(encrypted, quantum_key)
        assert decrypted == test_data

    def test_level_1_encryption_otp(self):
        """Test One-Time Pad encryption (Level 1)."""
        service = EncryptionService()
        test_data = "Short message"
        quantum_key = b'x' * len(test_data.encode('utf-8'))  # Key same length as data

        # Encrypt
        encrypted = service.encrypt_data(test_data, 1, quantum_key)
        assert encrypted['security_level'] == 1
        assert encrypted['algorithm'] == 'OTP'

        # Decrypt
        decrypted = service.decrypt_data(encrypted, quantum_key)
        assert decrypted == test_data

    def test_quantum_service_connection_check(self, client, test_user):
        """Test quantum service connection status."""
        # Login first
        client.post('/api/auth/login', json={
            'email': test_user.email,
            'password': 'password123'
        })

        response = client.get('/api/quantum/status')
        assert response.status_code == 200
        assert 'connected' in response.get_json()
        assert 'status' in response.get_json()

    def test_get_user_keys(self, client, test_user):
        """Test getting user's quantum keys."""
        # Login first
        client.post('/api/auth/login', json={
            'email': test_user.email,
            'password': 'password123'
        })

        response = client.get('/api/quantum/keys')
        assert response.status_code == 200
        assert 'keys' in response.get_json()