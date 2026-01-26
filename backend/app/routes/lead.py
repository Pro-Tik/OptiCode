"""
Lead Capture Routes
Handles Pathshala trial/lead form submissions.
"""
from flask import Blueprint, request

from app.extensions import db
from app.models import Lead
from app.utils import (
    validate_required_fields,
    error_response,
    success_response,
    require_json
)

lead_bp = Blueprint('lead', __name__)


@lead_bp.route('/lead', methods=['POST'])
@require_json
def capture_lead():
    """
    Capture a Pathshala trial lead.
    
    Expected JSON:
    {
        "name": "Jane Doe",
        "phone": "+1 555 000 0000",
        "school": "School Name (Optional)",
        "address": "123 Education Lane (Optional)"
    }
    
    Returns:
        JSON success response
    """
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'phone']
    is_valid, missing = validate_required_fields(data, required)
    
    if not is_valid:
        return error_response(f'Missing required fields: {", ".join(missing)}')
    
    # Clean and validate phone
    phone = data['phone'].strip()
    if len(phone) < 7:
        return error_response('Invalid phone number')
    
    # Create lead
    lead = Lead(
        name=data['name'].strip(),
        phone=phone,
        school=data.get('school', '').strip() or None,
        address=data.get('address', '').strip() or None
    )
    
    db.session.add(lead)
    db.session.commit()
    
    return success_response(
        data={'lead_id': lead.id},
        message='Lead captured successfully'
    )


@lead_bp.route('/leads', methods=['GET'])
def list_leads():
    """
    List all leads (for admin purposes).
    
    Query params:
        - limit: Number of leads to return (default: 50)
        - offset: Pagination offset (default: 0)
    
    Returns:
        JSON list of leads
    """
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Cap limit to prevent abuse
    limit = min(limit, 100)
    
    leads = Lead.query.order_by(Lead.created_at.desc()).offset(offset).limit(limit).all()
    total = Lead.query.count()
    
    return success_response(data={
        'leads': [lead.to_dict() for lead in leads],
        'total': total,
        'limit': limit,
        'offset': offset
    })
