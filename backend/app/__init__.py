"""
Flask Application Factory
Creates and configures the Flask application instance.
"""
import os
from flask import Flask, jsonify

from app.extensions import db, cors, migrate
from app.config import config


def create_app(config_name=None):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_name: Configuration to use ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    _init_extensions(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Register error handlers
    _register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def _init_extensions(app):
    """Initialize Flask extensions with the app instance."""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS with allowed origins
    cors.init_app(
        app,
        origins=app.config.get('CORS_ORIGINS', ['*']),
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    )


def _register_blueprints(app):
    """Register all application blueprints."""
    # API blueprints
    from app.routes.quote import quote_bp
    from app.routes.newsletter import newsletter_bp
    from app.routes.lead import lead_bp
    from app.routes.ticket import ticket_bp
    
    # Admin blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    
    # Main website blueprint
    from app.routes.main import main_bp
    
    # Register API routes with /api prefix
    app.register_blueprint(quote_bp, url_prefix='/api')
    app.register_blueprint(newsletter_bp, url_prefix='/api')
    app.register_blueprint(lead_bp, url_prefix='/api')
    app.register_blueprint(ticket_bp, url_prefix='/api')
    
    # Register admin routes with /admin prefix
    app.register_blueprint(auth_bp, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Register main website routes
    app.register_blueprint(main_bp)
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'OptiCode API is running'
        })


def _register_error_handlers(app):
    """Register custom error handlers."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error.description)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
