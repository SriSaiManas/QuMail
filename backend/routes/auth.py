from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import db
from backend.models.user import User
from backend.services.auth_service import AuthService
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
    try:
        data = request.get_json()

        # Input validation
        required_fields = ['email', 'password', 'full_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        email = data['email'].lower().strip()
        password = data['password']
        full_name = data['full_name'].strip()

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Validate password strength
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        user = auth_service.create_user(email, password, full_name)

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint."""
    try:
        data = request.get_json()

        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400

        email = data['email'].lower().strip()
        password = data['password']

        # Authenticate user
        user = auth_service.authenticate_user(email, password)

        if user:
            login_user(user, remember=data.get('remember', False))
            user.last_login = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint."""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check authentication status."""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200
    else:
        return jsonify({'authenticated': False}), 200


@auth_bp.route('/users/search', methods=['GET'])
@login_required
def search_users():
    """Search for users by email (for compose email validation)."""
    try:
        email = request.args.get('email', '').lower().strip()

        if not email:
            return jsonify({'error': 'Email parameter required'}), 400

        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({
                'found': True,
                'user': {
                    'email': user.email,
                    'full_name': user.full_name
                }
            }), 200
        else:
            return jsonify({'found': False}), 200

    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500