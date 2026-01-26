"""
Admin Dashboard Routes
Handles all admin panel pages and actions.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models import Ticket, Message, Lead, Subscriber
from app.routes.auth import login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
def dashboard():
    """Admin dashboard with statistics."""
    # Get ticket statistics
    total_tickets = Ticket.query.count()
    pending_tickets = Ticket.query.filter_by(status='Pending').count()
    accepted_tickets = Ticket.query.filter_by(status='Accepted').count()
    running_tickets = Ticket.query.filter_by(status='Running').count()
    completed_tickets = Ticket.query.filter_by(status='Completed').count()
    
    # Get other statistics
    total_leads = Lead.query.count()
    total_subscribers = Subscriber.query.filter_by(is_active=True).count()
    
    # Recent tickets
    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()
    
    # Recent leads
    recent_leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
        total_tickets=total_tickets,
        pending_tickets=pending_tickets,
        accepted_tickets=accepted_tickets,
        running_tickets=running_tickets,
        completed_tickets=completed_tickets,
        total_leads=total_leads,
        total_subscribers=total_subscribers,
        recent_tickets=recent_tickets,
        recent_leads=recent_leads
    )


@admin_bp.route('/tickets')
@login_required
def tickets():
    """List all tickets with filtering."""
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = Ticket.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    tickets = query.order_by(Ticket.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('tickets.html',
        tickets=tickets,
        status_filter=status_filter
    )


@admin_bp.route('/tickets/<ticket_id>')
@login_required
def ticket_detail(ticket_id):
    """View single ticket with messages."""
    ticket = Ticket.query.filter_by(ticket_id=ticket_id.upper()).first_or_404()
    messages = Message.query.filter_by(ticket_id=ticket.id).order_by(Message.created_at.asc()).all()
    
    return render_template('ticket_detail.html',
        ticket=ticket,
        messages=messages
    )


@admin_bp.route('/tickets/<ticket_id>/reply', methods=['POST'])
@login_required
def ticket_reply(ticket_id):
    """Send admin reply to ticket."""
    ticket = Ticket.query.filter_by(ticket_id=ticket_id.upper()).first_or_404()
    
    message_text = request.form.get('message', '').strip()
    
    if not message_text:
        flash('Message cannot be empty.', 'error')
        return redirect(url_for('admin.ticket_detail', ticket_id=ticket_id))
    
    message = Message(
        ticket_id=ticket.id,
        sender='admin',
        message=message_text
    )
    db.session.add(message)
    db.session.commit()
    
    flash('Reply sent successfully.', 'success')
    return redirect(url_for('admin.ticket_detail', ticket_id=ticket_id))


@admin_bp.route('/tickets/<ticket_id>/status', methods=['POST'])
@login_required
def ticket_status(ticket_id):
    """Update ticket status."""
    ticket = Ticket.query.filter_by(ticket_id=ticket_id.upper()).first_or_404()
    
    new_status = request.form.get('status')
    
    if new_status not in Ticket.VALID_STATUSES:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin.ticket_detail', ticket_id=ticket_id))
    
    ticket.status = new_status
    db.session.commit()
    
    flash(f'Status updated to {new_status}.', 'success')
    return redirect(url_for('admin.ticket_detail', ticket_id=ticket_id))


@admin_bp.route('/leads')
@login_required
def leads():
    """List all leads."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    leads = Lead.query.order_by(Lead.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('leads.html', leads=leads)


@admin_bp.route('/subscribers')
@login_required
def subscribers():
    """List all subscribers."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status_filter = request.args.get('status', 'all')
    
    query = Subscriber.query
    
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    
    subscribers = query.order_by(Subscriber.subscribed_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('subscribers.html',
        subscribers=subscribers,
        status_filter=status_filter
    )
