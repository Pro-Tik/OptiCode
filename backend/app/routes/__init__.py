"""
Routes Package
Exports all route blueprints.
"""
from app.routes.quote import quote_bp
from app.routes.newsletter import newsletter_bp
from app.routes.lead import lead_bp
from app.routes.ticket import ticket_bp
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp

__all__ = ['quote_bp', 'newsletter_bp', 'lead_bp', 'ticket_bp', 'auth_bp', 'admin_bp']
