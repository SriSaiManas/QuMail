from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from backend.models import db
from backend.models.user import User
import os

# Initialize extensions
login_manager = LoginManager()


def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__,
                static_folder='../frontend/static',
                template_folder='../frontend/templates')

    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    from backend.config import config
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.email_routes import email_bp
    from backend.routes.quantum_routes import quantum_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(email_bp, url_prefix='/api/email')
    app.register_blueprint(quantum_bp, url_prefix='/api/quantum')

    # Main routes
    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500

    # Create tables
    with app.app_context():
        db.create_all()

    return app


# For direct execution
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)