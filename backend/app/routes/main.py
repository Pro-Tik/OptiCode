"""
Main Routes
Serves the landing pages and static content.
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/pathshala.html')
def pathshala():
    return render_template('pathshala.html')

@main_bp.route('/status.html')
def status():
    return render_template('status.html')

@main_bp.route('/privacy.html')
def privacy():
    return render_template('privacy.html')

@main_bp.route('/terms.html')
def terms():
    return render_template('terms.html')

@main_bp.route('/refund.html')
def refund():
    return render_template('refund.html')

@main_bp.route('/ai-code-optimization-tool.html')
def ai_optimization():
    return render_template('ai-code-optimization-tool.html')

@main_bp.route('/ai-for-developers.html')
def ai_developers():
    return render_template('ai-for-developers.html')

@main_bp.route('/automated-code-cleaner.html')
def automated_cleaner():
    return render_template('automated-code-cleaner.html')
