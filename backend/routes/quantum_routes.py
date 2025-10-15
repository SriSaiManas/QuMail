from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.services.quantum_service import QuantumService
from flask import current_app

quantum_bp = Blueprint('quantum', __name__)


@quantum_bp.route('/status', methods=['GET'])
@login_required
def check_quantum_status():
    """Check quantum key manager connection status."""
    try:
        quantum_service = QuantumService(
            current_app.config['KM_BASE_URL'],
            current_app.config['KM_API_KEY']
        )

        status = quantum_service.check_km_connection()
        return jsonify(status), 200

    except Exception as e:
        return jsonify({
            'connected': False,
            'status': 'error',
            'error': str(e)
        }), 500


@quantum_bp.route('/keys', methods=['GET'])
@login_required
def get_user_keys():
    """Get user's quantum keys."""
    try:
        from backend.models.quantum_key import QuantumKey

        keys = QuantumKey.query.filter_by(user_id=current_user.id) \
            .order_by(QuantumKey.created_at.desc()).all()

        return jsonify({
            'keys': [key.to_dict() for key in keys]
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get keys: {str(e)}'}), 500


@quantum_bp.route('/keys/request', methods=['POST'])
@login_required
def request_quantum_key():
    """Request new quantum key."""
    try:
        data = request.get_json()

        recipient_email = data.get('recipient_email', '').lower().strip()
        key_length = data.get('key_length', 256)

        if not recipient_email:
            return jsonify({'error': 'Recipient email required'}), 400

        quantum_service = QuantumService(
            current_app.config['KM_BASE_URL'],
            current_app.config['KM_API_KEY']
        )

        key = quantum_service.get_quantum_key(
            current_user.id, recipient_email, key_length
        )

        if key:
            return jsonify({
                'success': True,
                'key': key.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to obtain quantum key'}), 400

    except Exception as e:
        return jsonify({'error': f'Failed to request key: {str(e)}'}), 500