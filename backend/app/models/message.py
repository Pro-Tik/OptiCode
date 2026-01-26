"""
Message Model
Stores messages exchanged on a ticket (support chat).
"""
from datetime import datetime
from app.extensions import db


class Message(db.Model):
    """
    Represents a message in a ticket conversation.
    
    Attributes:
        id: Primary key
        ticket_id: Foreign key to parent ticket
        sender: Message sender ('user' or 'admin')
        message: Message content
        created_at: Timestamp of creation
    """
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False, index=True)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'admin'
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Valid sender types
    SENDER_USER = 'user'
    SENDER_ADMIN = 'admin'
    
    def to_dict(self):
        """Convert message to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'sender': self.sender,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Message {self.id} on Ticket {self.ticket_id}>'
