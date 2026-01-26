"""
Utility Helpers
Common utility functions used across the application.
"""
import random
import string
from functools import wraps
from flask import request, jsonify


def generate_ticket_id():
    """
    Generate a unique ticket ID in OPT-XXXX format.
    
    Returns:
        str: Ticket ID like 'OPT-A1B2'
    """
    # Generate 4 random alphanumeric characters
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(4))
    return f'OPT-{random_part}'


def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present in the data.
    
    Args:
        data: Dictionary of submitted data
        required_fields: List of required field names
        
    Returns:
        tuple: (is_valid, missing_fields)
    """
    missing = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing.append(field)
    
    return len(missing) == 0, missing


def validate_email(email):
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email or '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    if not local or not domain:
        return False
    
    if '.' not in domain:
        return False
    
    return True


def json_response(data, status=200):
    """
    Create a standardized JSON response.
    
    Args:
        data: Dictionary to serialize
        status: HTTP status code
        
    Returns:
        Flask response object
    """
    response = jsonify(data)
    response.status_code = status
    return response


def error_response(message, status=400):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status: HTTP status code
        
    Returns:
        Flask response object
    """
    return json_response({
        'error': True,
        'message': message
    }, status)


def success_response(data=None, message='Success'):
    """
    Create a standardized success response.
    
    Args:
        data: Optional data to include
        message: Success message
        
    Returns:
        Flask response object
    """
    response_data = {
        'success': True,
        'message': message
    }
    if data:
        response_data.update(data)
    
    return json_response(response_data)


def require_json(f):
    """
    Decorator to require JSON content type for a route.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return error_response('Content-Type must be application/json', 400)
        return f(*args, **kwargs)
    return decorated_function
