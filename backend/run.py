#!/usr/bin/env python3
"""
Development Server Runner
Run this file to start the development server.
"""
from app import create_app

if __name__ == '__main__':
    app = create_app('development')
    
    print("\n" + "=" * 60)
    print("  OptiCode Backend API - Development Server")
    print("=" * 60)
    print("  Health Check: http://localhost:5000/api/health")
    print("  Endpoints:")
    print("    POST /api/quote       - Submit quote request")
    print("    POST /api/subscribe   - Newsletter subscription")
    print("    POST /api/lead        - Pathshala lead capture")
    print("    GET  /api/ticket/<id> - Get ticket details")
    print("    GET  /api/ticket/<id>/messages - Get messages")
    print("    POST /api/ticket/<id>/message  - Send message")
    print("=" * 60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5200,
        debug=True
    )
