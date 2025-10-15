from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import json
from typing import Tuple, Optional


class EncryptionService:
    """Multi-level encryption service for QuMail."""

    def __init__(self):
        self.fernet = None

    def encrypt_data(self, data: str, security_level: int, quantum_key: Optional[bytes] = None) -> dict:
        """
        Encrypt data based on security level.

        Args:
            data: The data to encrypt
            security_level: 1-4 (OTP, QKD-AES, PQC, Standard)
            quantum_key: Quantum key for levels 1 and 2

        Returns:
            dict: Encrypted data with metadata
        """
        try:
            data_bytes = data.encode('utf-8')

            if security_level == 1:  # Quantum Secure - One Time Pad
                return self._encrypt_otp(data_bytes, quantum_key)
            elif security_level == 2:  # Quantum-aided AES
                return self._encrypt_qkd_aes(data_bytes, quantum_key)
            elif security_level == 3:  # Post-Quantum Crypto (placeholder)
                return self._encrypt_pqc(data_bytes)
            else:  # Level 4 - Standard encryption
                return self._encrypt_standard(data_bytes)

        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt_data(self, encrypted_data: dict, quantum_key: Optional[bytes] = None) -> str:
        """
        Decrypt data based on security level.

        Args:
            encrypted_data: Dictionary containing encrypted data and metadata
            quantum_key: Quantum key for levels 1 and 2

        Returns:
            str: Decrypted data
        """
        try:
            security_level = encrypted_data.get('security_level')

            if security_level == 1:
                return self._decrypt_otp(encrypted_data, quantum_key)
            elif security_level == 2:
                return self._decrypt_qkd_aes(encrypted_data, quantum_key)
            elif security_level == 3:
                return self._decrypt_pqc(encrypted_data)
            else:
                return self._decrypt_standard(encrypted_data)

        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

    def _encrypt_otp(self, data: bytes, quantum_key: bytes) -> dict:
        """One-Time Pad encryption using quantum key."""
        if not quantum_key or len(quantum_key) < len(data):
            raise ValueError("Quantum key must be at least as long as the data")

        # XOR data with quantum key
        encrypted_bytes = bytes(a ^ b for a, b in zip(data, quantum_key[:len(data)]))

        return {
            'encrypted_data': base64.b64encode(encrypted_bytes).decode('utf-8'),
            'security_level': 1,
            'algorithm': 'OTP',
            'key_length_used': len(data)
        }

    def _decrypt_otp(self, encrypted_data: dict, quantum_key: bytes) -> str:
        """One-Time Pad decryption using quantum key."""
        if not quantum_key:
            raise ValueError("Quantum key required for OTP decryption")

        encrypted_bytes = base64.b64decode(encrypted_data['encrypted_data'])
        key_length_used = encrypted_data.get('key_length_used', len(encrypted_bytes))

        # XOR encrypted data with quantum key
        decrypted_bytes = bytes(a ^ b for a, b in zip(encrypted_bytes, quantum_key[:key_length_used]))

        return decrypted_bytes.decode('utf-8')

    def _encrypt_qkd_aes(self, data: bytes, quantum_key: bytes) -> dict:
        """AES encryption using quantum key as seed."""
        if not quantum_key or len(quantum_key) < 32:
            raise ValueError("Quantum key must be at least 32 bytes for AES")

        # Use quantum key as AES key (first 32 bytes)
        aes_key = quantum_key[:32]

        # Generate random IV
        iv = os.urandom(16)

        # Encrypt using AES-256-CBC
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        # Pad data to block size
        padded_data = self._pad_data(data)
        encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()

        return {
            'encrypted_data': base64.b64encode(encrypted_bytes).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'security_level': 2,
            'algorithm': 'AES-QKD'
        }

    def _decrypt_qkd_aes(self, encrypted_data: dict, quantum_key: bytes) -> str:
        """AES decryption using quantum key as seed."""
        if not quantum_key or len(quantum_key) < 32:
            raise ValueError("Quantum key required for AES-QKD decryption")

        aes_key = quantum_key[:32]
        iv = base64.b64decode(encrypted_data['iv'])
        encrypted_bytes = base64.b64decode(encrypted_data['encrypted_data'])

        # Decrypt using AES-256-CBC
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove padding
        unpadded_data = self._unpad_data(decrypted_bytes)

        return unpadded_data.decode('utf-8')

    def _encrypt_pqc(self, data: bytes) -> dict:
        """Post-Quantum Cryptography (placeholder implementation)."""
        # For now, using standard AES as placeholder
        key = os.urandom(32)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        padded_data = self._pad_data(data)
        encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()

        return {
            'encrypted_data': base64.b64encode(encrypted_bytes).decode('utf-8'),
            'key': base64.b64encode(key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'security_level': 3,
            'algorithm': 'PQC-AES'
        }

    def _decrypt_pqc(self, encrypted_data: dict) -> str:
        """Post-Quantum Cryptography decryption (placeholder)."""
        key = base64.b64decode(encrypted_data['key'])
        iv = base64.b64decode(encrypted_data['iv'])
        encrypted_bytes = base64.b64decode(encrypted_data['encrypted_data'])

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

        unpadded_data = self._unpad_data(decrypted_bytes)
        return unpadded_data.decode('utf-8')

    def _encrypt_standard(self, data: bytes) -> dict:
        """Standard encryption (no quantum security)."""
        key = Fernet.generate_key()
        fernet = Fernet(key)

        encrypted_bytes = fernet.encrypt(data)

        return {
            'encrypted_data': base64.b64encode(encrypted_bytes).decode('utf-8'),
            'key': base64.b64encode(key).decode('utf-8'),
            'security_level': 4,
            'algorithm': 'STANDARD'
        }

    def _decrypt_standard(self, encrypted_data: dict) -> str:
        """Standard decryption."""
        key = base64.b64decode(encrypted_data['key'])
        encrypted_bytes = base64.b64decode(encrypted_data['encrypted_data'])

        fernet = Fernet(key)
        decrypted_bytes = fernet.decrypt(encrypted_bytes)

        return decrypted_bytes.decode('utf-8')

    def _pad_data(self, data: bytes) -> bytes:
        """PKCS7 padding for block cipher."""
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad_data(self, padded_data: bytes) -> bytes:
        """Remove PKCS7 padding."""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]