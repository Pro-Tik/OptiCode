"""
Subscriber Model
Stores newsletter email subscriptions.
"""
from datetime import datetime
from app.extensions import db


class Subscriber(db.Model):
    """
    Represents a newsletter subscriber.
    
    Attributes:
        id: Primary key
        email: Subscriber email address (unique)
        is_active: Whether subscription is active
        subscribed_at: Timestamp of subscription
        unsubscribed_at: Timestamp of unsubscription (if applicable)
    """
    __tablename__ = 'subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    unsubscribed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        """Convert subscriber to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'subscribed_at': self.subscribed_at.isoformat() if self.subscribed_at else None
        }
    
    def __repr__(self):
        return f'<Subscriber {self.email}>'
