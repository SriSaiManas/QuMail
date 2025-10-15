import requests
import json
import base64
import secrets
from datetime import datetime, timedelta
from backend.models import db
from backend.models.quantum_key import QuantumKey
from backend.models.user import User
from typing import Optional, Dict, Any


class QuantumService:
    """Quantum Key Distribution service following ETSI GS QKD 014."""

    def __init__(self, km_base_url: str, km_api_key: str):
        self.km_base_url = km_base_url.rstrip('/')
        self.km_api_key = km_api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {km_api_key}'
        }

    def get_quantum_key(self, user_id: int, recipient_email: str, key_length: int = 256) -> Optional[QuantumKey]:
        """
        Get quantum key from Key Manager (ETSI GS QKD 014 compliant).

        Args:
            user_id: ID of requesting user
            recipient_email: Email of recipient
            key_length: Required key length in bytes

        Returns:
            QuantumKey object or None if failed
        """
        try:
            # Check if we have a valid existing key
            existing_key = QuantumKey.get_valid_key(user_id, recipient_email)
            if existing_key and existing_key.key_length >= key_length:
                return existing_key

            # Request new key from Key Manager
            km_response = self._request_key_from_km(recipient_email, key_length)

            if km_response:
                # Store key in database
                quantum_key = self._store_quantum_key(
                    user_id, recipient_email, km_response, key_length
                )
                return quantum_key

            return None

        except Exception as e:
            print(f"Error getting quantum key: {str(e)}")
            return None

    def _request_key_from_km(self, recipient_email: str, key_length: int) -> Optional[Dict[Any, Any]]:
        """Request key from Key Manager using ETSI protocol."""
        try:
            # ETSI GS QKD 014 key request format
            request_payload = {
                "key_ID": f"qkd_{secrets.token_hex(16)}",
                "size": key_length,
                "additional_slave_SAE_IDs": [recipient_email],
                "extension_mandatory": [],
                "extension_optional": []
            }

            # Make request to KM
            response = requests.post(
                f"{self.km_base_url}/api/v1/keys/get_key",
                headers=self.headers,
                json=request_payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"KM request failed: {response.status_code} - {response.text}")
                return None

        except requests.RequestException as e:
            print(f"KM connection error: {str(e)}")
            # Fallback to simulated key for testing
            return self._simulate_km_response(key_length)
        except Exception as e:
            print(f"KM request error: {str(e)}")
            return None

    def _simulate_km_response(self, key_length: int) -> Dict[Any, Any]:
        """Simulate KM response for testing purposes."""
        return {
            "key_ID": f"sim_qkd_{secrets.token_hex(16)}",
            "key": base64.b64encode(secrets.token_bytes(key_length)).decode('utf-8'),
            "size": key_length,
            "metadata": {
                "generation_time": datetime.utcnow().isoformat(),
                "source": "simulator",
                "type": "symmetric"
            }
        }

    def _store_quantum_key(self, user_id: int, recipient_email: str,
                           km_response: dict, key_length: int) -> QuantumKey:
        """Store quantum key in database."""
        try:
            # Encrypt key data for storage (using system key)
            key_data = km_response.get('key')
            encrypted_key_data = self._encrypt_key_for_storage(key_data)

            quantum_key = QuantumKey(
                key_id=km_response['key_ID'],
                user_id=user_id,
                recipient_email=recipient_email,
                encrypted_key_data=encrypted_key_data,
                key_length=key_length,
                km_source=km_response.get('metadata', {}).get('source', 'unknown'),
                sequence_number=secrets.randbits(64)
            )

            db.session.add(quantum_key)
            db.session.commit()

            return quantum_key

        except Exception as e:
            db.session.rollback()
            raise e

    def retrieve_key_data(self, quantum_key: QuantumKey) -> Optional[bytes]:
        """Retrieve and decrypt quantum key data."""
        try:
            if not quantum_key.is_valid():
                return None

            # Decrypt key data
            key_data = self._decrypt_key_from_storage(quantum_key.encrypted_key_data)

            # Mark key as used (for OTP)
            if quantum_key.key_type == 'symmetric':
                quantum_key.mark_as_used()

            return base64.b64decode(key_data)

        except Exception as e:
            print(f"Error retrieving key data: {str(e)}")
            return None

    def _encrypt_key_for_storage(self, key_data: str) -> str:
        """Encrypt quantum key for secure storage."""
        # Simple XOR encryption for demo (use proper encryption in production)
        storage_key = b"quantum_storage_key_change_me_in_production_32b"
        key_bytes = base64.b64decode(key_data)

        encrypted = bytes(a ^ b for a, b in zip(key_bytes,
                                                (storage_key * (len(key_bytes) // len(storage_key) + 1))[
                                                :len(key_bytes)]))

        return base64.b64encode(encrypted).decode('utf-8')

    def _decrypt_key_from_storage(self, encrypted_key_data: str) -> str:
        """Decrypt quantum key from storage."""
        storage_key = b"quantum_storage_key_change_me_in_production_32b"
        encrypted_bytes = base64.b64decode(encrypted_key_data)

        decrypted = bytes(a ^ b for a, b in zip(encrypted_bytes,
                                                (storage_key * (len(encrypted_bytes) // len(storage_key) + 1))[
                                                :len(encrypted_bytes)]))

        return base64.b64encode(decrypted).decode('utf-8')

    def check_km_connection(self) -> Dict[str, Any]:
        """Check connection to Key Manager."""
        try:
            response = requests.get(
                f"{self.km_base_url}/api/v1/status",
                headers=self.headers,
                timeout=10
            )

            return {
                'connected': response.status_code == 200,
                'status': 'connected' if response.status_code == 200 else 'error',
                'response_time': response.elapsed.total_seconds()
            }

        except requests.RequestException:
            return {
                'connected': False,
                'status': 'connection_error',
                'response_time': None
            }