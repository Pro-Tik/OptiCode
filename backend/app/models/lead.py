"""
Lead Model
Stores Pathshala trial/lead form submissions.
"""
from datetime import datetime
from app.extensions import db


class Lead(db.Model):
    """
    Represents a Pathshala trial lead.
    
    Attributes:
        id: Primary key
        name: Lead's full name
        phone: Contact phone number
        school: School/institution name (optional)
        address: School/company address (optional)
        created_at: Timestamp of submission
    """
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(200), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert lead to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'school': self.school,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Lead {self.name}>'
