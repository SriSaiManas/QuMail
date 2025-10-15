from . import db
from datetime import datetime, timedelta
import uuid


class QuantumKey(db.Model):
    __tablename__ = 'quantum_keys'

    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # Key Owner and Recipient
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False, index=True)

    # Key Data (encrypted in storage)
    encrypted_key_data = db.Column(db.Text, nullable=False)
    key_length = db.Column(db.Integer, nullable=False)
    key_type = db.Column(db.String(20), default='symmetric')  # symmetric, asymmetric

    # Key Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    used_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)

    # ETSI QKD Protocol Fields
    km_source = db.Column(db.String(100))  # Key Manager source
    sequence_number = db.Column(db.BigInteger)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.key_id:
            self.key_id = str(uuid.uuid4())
        if not self.expires_at:
            # Default expiration: 24 hours
            self.expires_at = datetime.utcnow() + timedelta(hours=24)

    def is_expired(self):
        """Check if key has expired."""
        return datetime.utcnow() > self.expires_at

    def is_valid(self):
        """Check if key is valid for use."""
        return not self.is_expired() and not self.is_used

    def mark_as_used(self):
        """Mark key as used."""
        self.is_used = True
        self.used_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convert key to dictionary."""
        return {
            'key_id': self.key_id,
            'recipient_email': self.recipient_email,
            'key_length': self.key_length,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_expired': self.is_expired(),
            'is_used': self.is_used,
            'is_valid': self.is_valid()
        }

    @staticmethod
    def get_valid_key(user_id, recipient_email):
        """Get a valid quantum key for recipient."""
        return QuantumKey.query.filter_by(
            user_id=user_id,
            recipient_email=recipient_email,
            is_used=False
        ).filter(
            QuantumKey.expires_at > datetime.utcnow()
        ).first()

    def __repr__(self):
        return f'<QuantumKey {self.key_id[:8]} for {self.recipient_email}>'