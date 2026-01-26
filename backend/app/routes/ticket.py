"""
Ticket/Status Portal Routes
Handles ticket retrieval and messaging for the status tracking portal.
"""
from flask import Blueprint, request

from app.extensions import db
from app.models import Ticket, Message
from app.utils import (
    validate_required_fields,
    error_response,
    success_response,
    json_response,
    require_json
)

ticket_bp = Blueprint('ticket', __name__)


@ticket_bp.route('/ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """
    Get ticket details by ticket ID.
    
    Args:
        ticket_id: Ticket ID (e.g., OPT-A1B2)
    
    Returns:
        JSON with ticket details
    """
    # Normalize ticket ID to uppercase
    ticket_id = ticket_id.strip().upper()
    
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    
    if not ticket:
        return error_response('Ticket not found', 404)
    
    return json_response(ticket.to_dict())


@ticket_bp.route('/ticket/<ticket_id>/messages', methods=['GET'])
def get_ticket_messages(ticket_id):
    """
    Get all messages for a ticket.
    
    Args:
        ticket_id: Ticket ID (e.g., OPT-A1B2)
    
    Returns:
        JSON array of messages
    """
    # Normalize ticket ID to uppercase
    ticket_id = ticket_id.strip().upper()
    
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    
    if not ticket:
        return error_response('Ticket not found', 404)
    
    messages = Message.query.filter_by(ticket_id=ticket.id).order_by(Message.created_at.asc()).all()
    
    return json_response([msg.to_dict() for msg in messages])


@ticket_bp.route('/ticket/<ticket_id>/message', methods=['POST'])
@require_json
def add_ticket_message(ticket_id):
    """
    Add a new message to a ticket conversation.
    
    Args:
        ticket_id: Ticket ID (e.g., OPT-A1B2)
    
    Expected JSON:
    {
        "sender": "user" | "admin",
        "message": "Message content..."
    }
    
    Returns:
        JSON with created message
    """
    # Normalize ticket ID to uppercase
    ticket_id = ticket_id.strip().upper()
    
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    
    if not ticket:
        return error_response('Ticket not found', 404)
    
    data = request.get_json()
    
    # Validate required fields
    required = ['sender', 'message']
    is_valid, missing = validate_required_fields(data, required)
    
    if not is_valid:
        return error_response(f'Missing required fields: {", ".join(missing)}')
    
    # Validate sender
    sender = data['sender'].lower()
    if sender not in [Message.SENDER_USER, Message.SENDER_ADMIN]:
        return error_response('Invalid sender. Must be "user" or "admin"')
    
    # Create message
    message = Message(
        ticket_id=ticket.id,
        sender=sender,
        message=data['message'].strip()
    )
    
    db.session.add(message)
    db.session.commit()
    
    return json_response(message.to_dict(), 201)


@ticket_bp.route('/ticket/<ticket_id>/status', methods=['PUT'])
@require_json
def update_ticket_status(ticket_id):
    """
    Update ticket status (admin endpoint).
    
    Args:
        ticket_id: Ticket ID (e.g., OPT-A1B2)
    
    Expected JSON:
    {
        "status": "Accepted" | "Running" | "Completed" | "Cancelled"
    }
    
    Returns:
        JSON with updated ticket
    """
    # Normalize ticket ID to uppercase
    ticket_id = ticket_id.strip().upper()
    
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    
    if not ticket:
        return error_response('Ticket not found', 404)
    
    data = request.get_json()
    
    status = data.get('status')
    if not status:
        return error_response('Status is required')
    
    if status not in Ticket.VALID_STATUSES:
        return error_response(f'Invalid status. Valid values: {", ".join(Ticket.VALID_STATUSES)}')
    
    ticket.status = status
    db.session.commit()
    
    return json_response(ticket.to_dict())


@ticket_bp.route('/tickets', methods=['GET'])
def list_tickets():
    """
    List all tickets (admin endpoint).
    
    Query params:
        - status: Filter by status
        - limit: Number of tickets to return (default: 50)
        - offset: Pagination offset (default: 0)
    
    Returns:
        JSON list of tickets
    """
    status = request.args.get('status')
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Cap limit
    limit = min(limit, 100)
    
    query = Ticket.query
    
    if status:
        query = query.filter_by(status=status)
    
    tickets = query.order_by(Ticket.created_at.desc()).offset(offset).limit(limit).all()
    total = query.count()
    
    return success_response(data={
        'tickets': [t.to_dict() for t in tickets],
        'total': total,
        'limit': limit,
        'offset': offset
    })
