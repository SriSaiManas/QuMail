from . import db
from datetime import datetime
import uuid


class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    # Sender and Recipient
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Email Content
    subject = db.Column(db.String(200), nullable=False)
    encrypted_body = db.Column(db.Text, nullable=False)  # Always encrypted
    encrypted_attachments = db.Column(db.Text)  # JSON string of encrypted attachments

    # Security Configuration
    security_level = db.Column(db.Integer, nullable=False, default=1)  # 1-4
    quantum_key_id = db.Column(db.String(100))  # Reference to quantum key used
    encryption_algorithm = db.Column(db.String(50), nullable=False)  # 'OTP', 'AES-QKD', 'PQC', 'STANDARD'

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime)
    is_decrypted = db.Column(db.Boolean, default=False)

    # Email Status
    status = db.Column(db.String(20), default='sent')  # sent, delivered, read, failed

    def to_dict(self):
        """Convert email to dictionary."""
        return {
            'id': self.id,
            'uuid': self.uuid,
            'sender_email': self.sender.email,
            'recipient_email': self.recipient.email,
            'subject': self.subject,
            'encrypted_body': self.encrypted_body,
            'security_level': self.security_level,
            'encryption_algorithm': self.encryption_algorithm,
            'created_at': self.created_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'status': self.status,
            'is_decrypted': self.is_decrypted
        }

    def mark_as_read(self):
        """Mark email as read."""
        if not self.read_at:
            self.read_at = datetime.utcnow()
            db.session.commit()

    def __repr__(self):
        return f'<Email {self.uuid[:8]} from {self.sender.email}>'