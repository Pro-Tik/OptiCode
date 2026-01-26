"""
Ticket Model
Stores quote/contact form submissions with tracking capability.
"""
from datetime import datetime
from app.extensions import db


class Ticket(db.Model):
    """
    Represents a quote/contact request ticket.
    
    Attributes:
        id: Primary key
        ticket_id: Human-readable ticket ID (OPT-XXXX format)
        name: Customer name
        email: Customer email
        project_type: Type of project/service requested
        message: Initial message from customer
        status: Current ticket status
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with messages
    messages = db.relationship('Message', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    
    # Valid status values
    STATUS_PENDING = 'Pending'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_RUNNING = 'Running'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'
    
    VALID_STATUSES = [STATUS_PENDING, STATUS_ACCEPTED, STATUS_RUNNING, STATUS_COMPLETED, STATUS_CANCELLED]
    
    def to_dict(self):
        """Convert ticket to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'name': self.name,
            'email': self.email,
            'project_type': self.project_type,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Ticket {self.ticket_id}>'
