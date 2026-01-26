"""
Newsletter Subscription Routes
Handles email subscriptions.
"""
from flask import Blueprint, request

from app.extensions import db
from app.models import Subscriber
from app.utils import (
    validate_email,
    error_response,
    success_response,
    require_json
)

newsletter_bp = Blueprint('newsletter', __name__)


@newsletter_bp.route('/subscribe', methods=['POST'])
@require_json
def subscribe():
    """
    Subscribe an email to the newsletter.
    
    Expected JSON:
    {
        "email": "user@example.com"
    }
    
    Returns:
        JSON success response
    """
    data = request.get_json()
    
    # Validate email
    email = data.get('email', '').strip().lower()
    
    if not email:
        return error_response('Email is required')
    
    if not validate_email(email):
        return error_response('Invalid email address')
    
    # Check if already subscribed
    existing = Subscriber.query.filter_by(email=email).first()
    
    if existing:
        if existing.is_active:
            # Already subscribed, return success silently
            return success_response(message='Already subscribed')
        else:
            # Reactivate subscription
            existing.is_active = True
            existing.unsubscribed_at = None
            db.session.commit()
            return success_response(message='Subscription reactivated')
    
    # Create new subscriber
    subscriber = Subscriber(email=email, is_active=True)
    db.session.add(subscriber)
    db.session.commit()
    
    return success_response(message='Successfully subscribed to newsletter')


@newsletter_bp.route('/unsubscribe', methods=['POST'])
@require_json
def unsubscribe():
    """
    Unsubscribe an email from the newsletter.
    
    Expected JSON:
    {
        "email": "user@example.com"
    }
    
    Returns:
        JSON success response
    """
    from datetime import datetime
    
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return error_response('Email is required')
    
    subscriber = Subscriber.query.filter_by(email=email).first()
    
    if not subscriber:
        return error_response('Email not found', 404)
    
    subscriber.is_active = False
    subscriber.unsubscribed_at = datetime.utcnow()
    db.session.commit()
    
    return success_response(message='Successfully unsubscribed')
