from backend.models import db
from backend.models.user import User
from werkzeug.security import check_password_hash


class AuthService:
    """Authentication service for user management."""

    def create_user(self, email, password, full_name):
        """Create a new user."""
        try:
            user = User(
                email=email.lower().strip(),
                full_name=full_name.strip()
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            db.session.rollback()
            raise e

    def authenticate_user(self, email, password):
        """Authenticate user with email and password."""
        try:
            user = User.query.filter_by(email=email.lower().strip()).first()

            if user and user.check_password(password) and user.is_active:
                return user
            return None
        except Exception as e:
            return None

    def get_user_by_email(self, email):
        """Get user by email."""
        return User.query.filter_by(email=email.lower().strip()).first()

    def deactivate_user(self, user_id):
        """Deactivate user account."""
        try:
            user = User.query.get(user_id)
            if user:
                user.is_active = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False