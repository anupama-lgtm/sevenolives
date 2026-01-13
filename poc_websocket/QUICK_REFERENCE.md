# Quick Reference Card - Django WebSocket POC

## 🚀 Quick Start (3 Steps)

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Django
cd poc_websocket
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Browser: Open both windows
# http://localhost:8000/window1/
# http://localhost:8000/window2/
```

## 📁 Project Structure

```
poc_websocket/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── db.sqlite3            # Database (auto-created)
├── poc_project/          # Django project
│   ├── settings.py       # Configuration
│   ├── urls.py          # URL routing
│   └── asgi.py          # ASGI config
├── user_app/            # Main app
│   ├── models.py        # User model
│   ├── views.py         # API + pages
│   ├── consumers.py     # WebSocket
│   ├── serializers.py   # DRF serializers
│   └── routing.py       # WS routing
└── templates/           # HTML templates
    ├── window1.html     # First name edit
    └── window2.html     # Last name edit
```

## 🔧 Common Commands

```bash
# Setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver
python manage.py runserver 8080  # Custom port

# Database
python manage.py shell
python create_sample_data.py

# Check Redis
python check_redis.py

# Utilities
python manage.py dbshell        # SQL shell
python manage.py showmigrations # Show migrations
```

## 🌐 URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000/ | Redirects to Window 1 |
| http://localhost:8000/window1/ | Window 1 (Edit First Name) |
| http://localhost:8000/window2/ | Window 2 (Edit Last Name) |
| http://localhost:8000/admin/ | Django Admin |
| http://localhost:8000/api/users/ | User API List |
| http://localhost:8000/api/users/1/ | User API Detail |
| ws://localhost:8000/ws/user-updates/ | WebSocket |

## 🔌 API Examples

### List Users
```bash
curl http://localhost:8000/api/users/
```

### Get User
```bash
curl http://localhost:8000/api/users/1/
```

### Create User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe"}'
```

### Update First Name (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Johnny"}'
```

### Update Last Name (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"last_name":"Smith"}'
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/1/
```

## 💻 Python Shell Examples

```python
python manage.py shell

# Import models
from user_app.models import User

# Create user
User.objects.create(first_name="John", last_name="Doe")

# Get all users
User.objects.all()

# Get specific user
user = User.objects.get(id=1)

# Update user
user.first_name = "Johnny"
user.save()

# Delete user
user.delete()

# Filter users
User.objects.filter(first_name__startswith="J")

# Count users
User.objects.count()
```

## 🐛 Debugging

### Check WebSocket Connection
```javascript
// Browser Console
// Should see green status: "🟢 Connected"
console.log(ws.readyState)  // 1 = OPEN
```

### Check Redis Connection
```bash
redis-cli ping  # Should return: PONG
```

### Check Database
```bash
python manage.py dbshell
sqlite> .tables
sqlite> SELECT * FROM users;
sqlite> .quit
```

### View Server Logs
```bash
# Django prints logs to terminal
# Look for:
# - WebSocket CONNECT
# - WebSocket DISCONNECT
# - API requests (GET, POST, PATCH)
```

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Redis connection error | `redis-server` |
| WebSocket won't connect | Check Redis running |
| Port 8000 in use | `netstat -ano \| findstr :8000` |
| Module not found | `pip install -r requirements.txt` |
| Database locked | Close other connections |
| Changes not syncing | Refresh page, check WS status |
| Static files not loading | `python manage.py collectstatic` |

## 📊 Status Indicators

| Indicator | Meaning |
|-----------|---------|
| 🟢 Connected to WebSocket | Working correctly |
| 🔴 WebSocket Disconnected | Redis not running |
| Green badge "Editable" | You can edit this field |
| Gray badge "Read Only" | Synced from other window |

## 🎨 UI Features

### Window 1
- ✏️ **Editable**: First Name
- 🔒 **Read-only**: Last Name
- 🎨 **Theme**: Purple gradient

### Window 2
- 🔒 **Read-only**: First Name
- ✏️ **Editable**: Last Name
- 🎨 **Theme**: Pink gradient

## 🔒 Security Notes

⚠️ **This is a POC - NOT production-ready!**

Missing:
- Authentication
- Authorization
- CSRF protection for API
- Rate limiting
- Input sanitization
- HTTPS/WSS

## 📦 Dependencies

```
Django==4.2.9           # Web framework
channels==4.0.0         # WebSocket
channels-redis==4.1.0   # Redis backend
djangorestframework==3.14.0  # REST API
daphne==4.0.0          # ASGI server
redis==5.0.1           # Redis client
```

## 🧪 Test Checklist

- [ ] Open both windows
- [ ] Check green WebSocket status
- [ ] Edit First Name in Window 1 → See in Window 2
- [ ] Edit Last Name in Window 2 → See in Window 1
- [ ] Create new user → Appears in both
- [ ] Refresh pages → Data persists
- [ ] Stop Redis → Status turns red
- [ ] Start Redis → Auto-reconnects

## 📝 Code Snippets

### Create Migration
```bash
python manage.py makemigrations user_app
```

### Reset Database
```bash
python manage.py flush
```

### Export Users
```python
from user_app.models import User
import json

users = User.objects.all().values()
print(json.dumps(list(users), indent=2))
```

### WebSocket Test (Browser Console)
```javascript
// Manual WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/user-updates/');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

## 🎯 Key Concepts

1. **PATCH vs PUT**: PATCH updates partial data, PUT replaces entire resource
2. **WebSocket**: Bidirectional persistent connection
3. **Channel Layer**: Message distribution system (Redis)
4. **ASGI**: Async server interface (vs WSGI)
5. **Real-time**: Updates propagate instantly via WebSocket

## 📚 Useful Links

- Django: https://docs.djangoproject.com/
- Channels: https://channels.readthedocs.io/
- DRF: https://www.django-rest-framework.org/
- Redis: https://redis.io/

---

**Need help?** Check `README.md`, `TESTING_GUIDE.md`, or `ARCHITECTURE.md`

