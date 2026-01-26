# OptiCode Flask Backend

Professional and scalable Flask backend for the OptiCode website.

## Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run Development Server

```bash
python run.py
```

The server will start at `http://localhost:5000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/quote` | POST | Submit quote/contact form |
| `/api/subscribe` | POST | Newsletter subscription |
| `/api/unsubscribe` | POST | Newsletter unsubscription |
| `/api/lead` | POST | Pathshala lead capture |
| `/api/leads` | GET | List leads (admin) |
| `/api/ticket/<id>` | GET | Get ticket details |
| `/api/ticket/<id>/messages` | GET | Get ticket messages |
| `/api/ticket/<id>/message` | POST | Send message on ticket |
| `/api/ticket/<id>/status` | PUT | Update ticket status (admin) |
| `/api/tickets` | GET | List all tickets (admin) |

## Project Structure

```
backend/
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── config.py        # Configuration classes
│   ├── extensions.py    # Flask extensions
│   ├── models/          # Database models
│   │   ├── ticket.py
│   │   ├── message.py
│   │   ├── subscriber.py
│   │   └── lead.py
│   ├── routes/          # API blueprints
│   │   ├── quote.py
│   │   ├── newsletter.py
│   │   ├── lead.py
│   │   └── ticket.py
│   └── utils/           # Utility functions
│       └── helpers.py
├── .env                 # Environment variables
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── run.py              # Development server
└── wsgi.py             # Production WSGI entry
```

## Deployment to PythonAnywhere

1. Upload the `backend/` folder to PythonAnywhere
2. Create a MySQL database in the Databases tab
3. Update `.env` with production settings:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secure-random-key
   DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere-services.com/username$dbname
   ```
4. Configure WSGI file in Web tab to point to `wsgi.py`
5. Reload the web app

## Testing Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Submit quote
curl -X POST http://localhost:5000/api/quote \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","project_type":"Web Development","message":"Test message"}'

# Subscribe to newsletter
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'

# Get ticket
curl http://localhost:5000/api/ticket/OPT-XXXX
```
# OpticodeFullStack
