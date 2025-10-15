from backend.models import db
from backend.models.email import Email
from backend.models.user import User
from backend.services.encryption_service import EncryptionService
from backend.services.quantum_service import QuantumService
from flask import current_app
import json
from datetime import datetime
from typing import List, Optional, Dict, Any


class EmailService:
    """Email processing service with quantum encryption."""

    def __init__(self):
        self.encryption_service = EncryptionService()
        self.quantum_service = None

    def _get_quantum_service(self):
        """Lazy initialization of quantum service."""
        if not self.quantum_service:
            self.quantum_service = QuantumService(
                current_app.config['KM_BASE_URL'],
                current_app.config['KM_API_KEY']
            )
        return self.quantum_service

    def send_email(self, sender_id: int, recipient_email: str, subject: str,
                   body: str, security_level: int, attachments: List[Dict] = None) -> Dict[str, Any]:
        """
        Send encrypted email.

        Args:
            sender_id: ID of sender
            recipient_email: Email of recipient
            subject: Email subject
            body: Email body
            security_level: 1-4 security level
            attachments: List of attachment data

        Returns:
            Dict with email info or error
        """
        try:
            # Validate recipient
            recipient = User.query.filter_by(email=recipient_email.lower()).first()
            if not recipient:
                return {'error': 'Recipient not found', 'status': 'failed'}

            # Get quantum key if needed (levels 1 & 2)
            quantum_key = None
            if security_level in [1, 2]:
                key_length = len(body.encode('utf-8')) if security_level == 1 else 256
                quantum_key_obj = self._get_quantum_service().get_quantum_key(
                    sender_id, recipient_email, key_length
                )

                if not quantum_key_obj:
                    return {'error': 'Failed to obtain quantum key', 'status': 'failed'}

                quantum_key = self._get_quantum_service().retrieve_key_data(quantum_key_obj)
                quantum_key_id = quantum_key_obj.key_id
            else:
                quantum_key_id = None

            # Encrypt email body
            encrypted_body_data = self.encryption_service.encrypt_data(
                body, security_level, quantum_key
            )

            # Encrypt attachments if present
            encrypted_attachments = None
            if attachments:
                encrypted_attachments = self._encrypt_attachments(
                    attachments, security_level, quantum_key
                )

            # Create email record
            email = Email(
                sender_id=sender_id,
                recipient_id=recipient.id,
                subject=subject,
                encrypted_body=json.dumps(encrypted_body_data),
                encrypted_attachments=json.dumps(encrypted_attachments) if encrypted_attachments else None,
                security_level=security_level,
                quantum_key_id=quantum_key_id,
                encryption_algorithm=encrypted_body_data.get('algorithm', 'UNKNOWN'),
                status='sent'
            )

            db.session.add(email)
            db.session.commit()

            return {
                'success': True,
                'email_id': email.id,
                'email_uuid': email.uuid,
                'status': 'sent',
                'security_level': security_level,
                'encryption_algorithm': email.encryption_algorithm
            }

        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to send email: {str(e)}', 'status': 'failed'}

    def get_user_emails(self, user_id: int, folder: str = 'inbox') -> List[Dict[str, Any]]:
        """Get user's emails from specified folder."""
        try:
            if folder == 'inbox':
                emails = Email.query.filter_by(recipient_id=user_id) \
                    .order_by(Email.created_at.desc()).all()
            elif folder == 'outbox':
                emails = Email.query.filter_by(sender_id=user_id) \
                    .order_by(Email.created_at.desc()).all()
            else:
                return []

            return [email.to_dict() for email in emails]

        except Exception as e:
            print(f"Error getting emails: {str(e)}")
            return []

    def decrypt_email(self, email_id: int, user_id: int) -> Dict[str, Any]:
        """
        Decrypt email for authorized user.

        Args:
            email_id: Email ID to decrypt
            user_id: ID of requesting user

        Returns:
            Dict with decrypted content or error
        """
        try:
            # Get email and verify access
            email = Email.query.get(email_id)
            if not email:
                return {'error': 'Email not found'}

            if email.recipient_id != user_id and email.sender_id != user_id:
                return {'error': 'Access denied'}

            # Get quantum key if needed
            quantum_key = None
            if email.security_level in [1, 2] and email.quantum_key_id:
                quantum_key_obj = QuantumKey.query.filter_by(
                    key_id=email.quantum_key_id
                ).first()

                if not quantum_key_obj:
                    return {'error': 'Quantum key not found'}

                if not quantum_key_obj.is_valid():
                    return {'error': 'Quantum key expired or invalid'}

                quantum_key = self._get_quantum_service().retrieve_key_data(quantum_key_obj)

            # Decrypt email body
            encrypted_body_data = json.loads(email.encrypted_body)
            decrypted_body = self.encryption_service.decrypt_data(
                encrypted_body_data, quantum_key
            )

            # Decrypt attachments if present
            decrypted_attachments = None
            if email.encrypted_attachments:
                encrypted_attachments = json.loads(email.encrypted_attachments)
                decrypted_attachments = self._decrypt_attachments(
                    encrypted_attachments, email.security_level, quantum_key
                )

            # Mark as read if recipient is decrypting
            if email.recipient_id == user_id:
                email.mark_as_read()
                email.is_decrypted = True
                db.session.commit()

            return {
                'success': True,
                'email': email.to_dict(),
                'decrypted_body': decrypted_body,
                'decrypted_attachments': decrypted_attachments,
                'security_level': email.security_level
            }

        except Exception as e:
            return {'error': f'Decryption failed: {str(e)}'}

    def _encrypt_attachments(self, attachments: List[Dict], security_level: int,
                             quantum_key: Optional[bytes]) -> List[Dict]:
        """Encrypt email attachments."""
        encrypted_attachments = []

        for attachment in attachments:
            try:
                # Convert file data to string if needed
                file_data = attachment.get('data', '')
                if isinstance(file_data, bytes):
                    file_data = file_data.decode('latin-1')  # Preserve binary data

                encrypted_data = self.encryption_service.encrypt_data(
                    file_data, security_level, quantum_key
                )

                encrypted_attachments.append({
                    'filename': attachment.get('filename'),
                    'content_type': attachment.get('content_type'),
                    'size': attachment.get('size'),
                    'encrypted_data': encrypted_data
                })

            except Exception as e:
                print(f"Error encrypting attachment: {str(e)}")
                continue

        return encrypted_attachments

    def _decrypt_attachments(self, encrypted_attachments: List[Dict],
                             security_level: int, quantum_key: Optional[bytes]) -> List[Dict]:
        """Decrypt email attachments."""
        decrypted_attachments = []

        for attachment in encrypted_attachments:
            try:
                encrypted_data = attachment.get('encrypted_data')
                decrypted_data = self.encryption_service.decrypt_data(
                    encrypted_data, quantum_key
                )

                decrypted_attachments.append({
                    'filename': attachment.get('filename'),
                    'content_type': attachment.get('content_type'),
                    'size': attachment.get('size'),
                    'data': decrypted_data
                })

            except Exception as e:
                print(f"Error decrypting attachment: {str(e)}")
                continue

        return decrypted_attachments