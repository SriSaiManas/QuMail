from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.services.email_service import EmailService
import base64

email_bp = Blueprint('email', __name__)
email_service = EmailService()


@email_bp.route('/send', methods=['POST'])
@login_required
def send_email():
    """Send encrypted email endpoint."""
    try:
        data = request.get_json()

        # Input validation
        required_fields = ['recipient_email', 'subject', 'body', 'security_level']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        recipient_email = data['recipient_email'].lower().strip()
        subject = data['subject'].strip()
        body = data['body']
        security_level = int(data['security_level'])

        if security_level not in [1, 2, 3, 4]:
            return jsonify({'error': 'Invalid security level'}), 400

        # Handle attachments
        attachments = []
        if 'attachments' in data and data['attachments']:
            for attachment in data['attachments']:
                attachments.append({
                    'filename': attachment.get('filename'),
                    'content_type': attachment.get('content_type'),
                    'size': attachment.get('size'),
                    'data': attachment.get('data')  # Base64 encoded data
                })

        # Send email
        result = email_service.send_email(
            sender_id=current_user.id,
            recipient_email=recipient_email,
            subject=subject,
            body=body,
            security_level=security_level,
            attachments=attachments if attachments else None
        )

        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500


@email_bp.route('/inbox', methods=['GET'])
@login_required
def get_inbox():
    """Get user's inbox."""
    try:
        emails = email_service.get_user_emails(current_user.id, 'inbox')
        return jsonify({'emails': emails}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get inbox: {str(e)}'}), 500


@email_bp.route('/outbox', methods=['GET'])
@login_required
def get_outbox():
    """Get user's outbox."""
    try:
        emails = email_service.get_user_emails(current_user.id, 'outbox')
        return jsonify({'emails': emails}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get outbox: {str(e)}'}), 500


@email_bp.route('/<int:email_id>/decrypt', methods=['POST'])
@login_required
def decrypt_email(email_id):
    """Decrypt email endpoint."""
    try:
        result = email_service.decrypt_email(email_id, current_user.id)

        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'error': f'Failed to decrypt email: {str(e)}'}), 500


@email_bp.route('/<int:email_id>', methods=['GET'])
@login_required
def get_email(email_id):
    """Get email details (encrypted)."""
    try:
        from backend.models.email import Email

        email = Email.query.get(email_id)
        if not email:
            return jsonify({'error': 'Email not found'}), 404

        # Check access permissions
        if email.recipient_id != current_user.id and email.sender_id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403

        return jsonify({'email': email.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get email: {str(e)}'}), 500