# Django WebSocket POC - Two Window Sync

This is a Proof of Concept (POC) demonstrating real-time data synchronization between two windows using Django, WebSockets, and PATCH API calls.

## Features

- **Window 1**: Edit First Name (editable) + Last Name (read-only)
- **Window 2**: Edit Last Name (editable) + First Name (read-only)
- Real-time synchronization using WebSockets (Django Channels)
- PATCH API endpoint for partial updates
- SQLite database backend
- Beautiful, modern UI with gradient backgrounds

## Architecture

- **Backend**: Django 4.2.9 + Django REST Framework
- **WebSocket**: Django Channels 4.0.0 + Redis
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **API**: RESTful PATCH endpoint for updates

## Prerequisites

- Python 3.8+
- Redis server (for WebSocket message broker)

## Installation

### 1. Install Redis (if not already installed)

**Windows:**
```bash
# Download from https://github.com/microsoftarchive/redis/releases
# Or use WSL/Docker
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
```

### 2. Setup Python Environment

```bash
# Navigate to project directory
cd poc_websocket

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Django

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser

# Create initial user data (optional)
python manage.py shell
```

In Django shell:
```python
from user_app.models import User
User.objects.create(first_name="John", last_name="Doe")
User.objects.create(first_name="Jane", last_name="Smith")
exit()
```

### 4. Start Redis Server

```bash
# In a separate terminal
redis-server
```

### 5. Run Django Server

```bash
# Start the server with Daphne (ASGI server)
python manage.py runserver
```

## Usage

1. Open your browser and navigate to:
   - **Window 1**: http://localhost:8000/window1/
   - **Window 2**: http://localhost:8000/window2/

2. Open both URLs in separate browser windows/tabs

3. Test the real-time sync:
   - In Window 1: Edit the **First Name** field
   - Observe: The change appears in Window 2's First Name (read-only) field
   - In Window 2: Edit the **Last Name** field
   - Observe: The change appears in Window 1's Last Name (read-only) field

## API Endpoints

### List/Create Users
- **GET** `/api/users/` - List all users
- **POST** `/api/users/` - Create a new user

### User Detail
- **GET** `/api/users/<id>/` - Get user details
- **PATCH** `/api/users/<id>/` - Update user (partial update)
- **DELETE** `/api/users/<id>/` - Delete user

### WebSocket
- **ws://localhost:8000/ws/user-updates/** - Real-time updates

## How It Works

1. **User Updates Field**: 
   - JavaScript detects the change
   - Sends PATCH request to `/api/users/<id>/`
   - Backend updates database

2. **Backend Broadcasts**:
   - After saving to DB, backend sends message to WebSocket channel layer
   - All connected clients receive the update

3. **Client Updates UI**:
   - WebSocket message is received
   - JavaScript updates the corresponding field in real-time
   - Read-only fields are updated automatically

## Project Structure

```
poc_websocket/
├── manage.py
├── requirements.txt
├── README.md
├── poc_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── user_app/
│   ├── __init__.py
│   ├── models.py          # User model
│   ├── views.py           # API views + Page views
│   ├── serializers.py     # DRF serializers
│   ├── consumers.py       # WebSocket consumers
│   ├── routing.py         # WebSocket routing
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
└── templates/
    ├── window1.html       # Window 1 UI
    └── window2.html       # Window 2 UI
```

## Testing

1. Create a user in Window 1
2. Edit first name in Window 1 → Check Window 2 updates
3. Edit last name in Window 2 → Check Window 1 updates
4. Open browser console to see WebSocket messages
5. Test with multiple browser windows simultaneously

## Troubleshooting

### Redis Connection Error
```
Error: Cannot connect to Redis
```
**Solution**: Make sure Redis server is running (`redis-server`)

### WebSocket Connection Failed
```
Error: WebSocket connection failed
```
**Solution**: 
- Check if Django server is running with ASGI support
- Ensure CHANNEL_LAYERS is configured correctly in settings.py

### No Real-time Updates
**Solution**:
- Check browser console for WebSocket connection status
- Verify Redis is running
- Check if both windows are connected to WebSocket

## Production Considerations

For production deployment:

1. **Change SECRET_KEY** in settings.py
2. **Set DEBUG = False**
3. **Configure ALLOWED_HOSTS**
4. **Use PostgreSQL/MySQL** instead of SQLite
5. **Use production Redis** (Redis Cloud, AWS ElastiCache)
6. **Use HTTPS/WSS** for secure connections
7. **Add authentication/authorization**
8. **Add CSRF protection** for APIs
9. **Use Nginx/Apache** as reverse proxy
10. **Deploy with Gunicorn + Daphne**

## License

This is a POC project for demonstration purposes.

