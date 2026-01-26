"""
Quote/Contact Form Routes
Handles quote request submissions and ticket creation.
"""
from flask import Blueprint, request

from app.extensions import db
from app.models import Ticket, Message
from app.utils import (
    generate_ticket_id,
    validate_required_fields,
    validate_email,
    error_response,
    success_response,
    require_json
)

quote_bp = Blueprint('quote', __name__)


@quote_bp.route('/quote', methods=['POST'])
@require_json
def create_quote():
    """
    Create a new quote request ticket.
    
    Expected JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "project_type": "Web Development",
        "message": "I need a website..."
    }
    
    Returns:
        JSON with ticket_id for tracking
    """
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'email', 'project_type', 'message']
    is_valid, missing = validate_required_fields(data, required)
    
    if not is_valid:
        return error_response(f'Missing required fields: {", ".join(missing)}')
    
    # Validate email
    if not validate_email(data['email']):
        return error_response('Invalid email address')
    
    # Generate unique ticket ID
    ticket_id = generate_ticket_id()
    
    # Ensure ticket ID is unique (regenerate if collision)
    while Ticket.query.filter_by(ticket_id=ticket_id).first():
        ticket_id = generate_ticket_id()
    
    # Create ticket
    ticket = Ticket(
        ticket_id=ticket_id,
        name=data['name'].strip(),
        email=data['email'].strip().lower(),
        project_type=data['project_type'],
        message=data['message'].strip(),
        status=Ticket.STATUS_PENDING
    )
    
    db.session.add(ticket)
    
    # Add initial message to conversation
    initial_message = Message(
        ticket=ticket,
        sender=Message.SENDER_USER,
        message=data['message'].strip()
    )
    db.session.add(initial_message)
    
    db.session.commit()
    
    return success_response(
        data={'ticket_id': ticket_id},
        message='Quote request submitted successfully'
    )
