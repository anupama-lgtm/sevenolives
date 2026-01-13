# Architecture Documentation - Django WebSocket POC

## System Overview

This POC demonstrates real-time bidirectional data synchronization between two browser windows using WebSockets, with database persistence via Django ORM and RESTful API updates via PATCH requests.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                              │
├─────────────────────────────────┬───────────────────────────────┤
│                                 │                                │
│  ┌───────────────────────────┐  │  ┌───────────────────────────┐│
│  │      WINDOW 1 (Browser)   │  │  │      WINDOW 2 (Browser)   ││
│  │                           │  │  │                           ││
│  │  • First Name [EDITABLE]  │  │  │  • First Name [READONLY]  ││
│  │  • Last Name  [READONLY]  │  │  │  • Last Name  [EDITABLE]  ││
│  │                           │  │  │                           ││
│  │  ┌─────────────────────┐  │  │  │  ┌─────────────────────┐ ││
│  │  │  JavaScript Client  │  │  │  │  │  JavaScript Client  │ ││
│  │  │  - PATCH API calls  │  │  │  │  │  - PATCH API calls  │ ││
│  │  │  - WebSocket client │  │  │  │  │  - WebSocket client │ ││
│  │  │  - UI updates       │  │  │  │  │  - UI updates       │ ││
│  │  └─────────────────────┘  │  │  │  └─────────────────────┘ ││
│  └───────────────────────────┘  │  └───────────────────────────┘│
└─────────────────────────────────┴───────────────────────────────┘
                    │                           │
                    │ HTTP/WS                   │ HTTP/WS
                    ▼                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         SERVER SIDE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               Django Application (ASGI)                   │   │
│  │                                                            │   │
│  │  ┌──────────────────┐      ┌──────────────────────────┐  │   │
│  │  │   HTTP Endpoint  │      │   WebSocket Consumer     │  │   │
│  │  │                  │      │                          │  │   │
│  │  │  • GET  /api/    │      │  • Connect/Disconnect    │  │   │
│  │  │  • POST /api/    │      │  • Receive messages      │  │   │
│  │  │  • PATCH /api/   │◄─────┤  • Broadcast to group    │  │   │
│  │  │  • DELETE /api/  │      │                          │  │   │
│  │  └────────┬─────────┘      └───────────┬──────────────┘  │   │
│  │           │                            │                  │   │
│  │           ▼                            ▼                  │   │
│  │  ┌──────────────────┐      ┌─────────────────────────┐   │   │
│  │  │   Django ORM     │      │   Channels Layer        │   │   │
│  │  │                  │      │   (Redis Backend)       │   │   │
│  │  │  • User Model    │      │                         │   │   │
│  │  │  • Serializers   │      │  • Group management     │   │   │
│  │  │  • Save/Retrieve │      │  • Message broadcasting │   │   │
│  │  └────────┬─────────┘      └─────────────────────────┘   │   │
│  └───────────┼─────────────────────────────────────────────┘   │
│              │                            │                     │
│              ▼                            ▼                     │
│  ┌──────────────────┐          ┌─────────────────────────┐     │
│  │  SQLite Database │          │   Redis Server          │     │
│  │                  │          │                         │     │
│  │  • users table   │          │  • Channel groups       │     │
│  │  • Persistent    │          │  • Message queue        │     │
│  │    storage       │          │  • Pub/Sub              │     │
│  └──────────────────┘          └─────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Scenario 1: User Updates First Name in Window 1

```
1. User types in First Name field (Window 1)
   └─> onChange event triggered

2. JavaScript makes PATCH request
   └─> fetch('/api/users/1/', {method: 'PATCH', body: {first_name: "New"}})

3. Django View receives request
   └─> Validates data with UserSerializer
   └─> Saves to database via ORM
   └─> Returns updated user data

4. Django View broadcasts to WebSocket
   └─> channel_layer.group_send('user_updates', {...})

5. Redis distributes message to all connected clients

6. WebSocket Consumer receives message
   └─> Sends to all connected WebSocket clients

7. JavaScript receives WebSocket message (Window 1 & 2)
   └─> Parses JSON data
   └─> Updates UI (readonly field in Window 2)

Result: Window 2 shows updated First Name in readonly field
```

### Scenario 2: User Updates Last Name in Window 2

```
1. User types in Last Name field (Window 2)
   └─> onChange event triggered

2. JavaScript makes PATCH request
   └─> fetch('/api/users/1/', {method: 'PATCH', body: {last_name: "New"}})

3. Django View receives request
   └─> Validates data with UserSerializer
   └─> Saves to database via ORM
   └─> Returns updated user data

4. Django View broadcasts to WebSocket
   └─> channel_layer.group_send('user_updates', {...})

5. Redis distributes message to all connected clients

6. WebSocket Consumer receives message
   └─> Sends to all connected WebSocket clients

7. JavaScript receives WebSocket message (Window 1 & 2)
   └─> Parses JSON data
   └─> Updates UI (readonly field in Window 1)

Result: Window 1 shows updated Last Name in readonly field
```

## Technology Stack

### Backend
- **Django 4.2.9**: Web framework
- **Django REST Framework 3.14.0**: RESTful API
- **Django Channels 4.0.0**: WebSocket support
- **Daphne 4.0.0**: ASGI server
- **channels-redis 4.1.0**: Channel layer backend

### Database
- **SQLite**: Default (production: PostgreSQL/MySQL)
- **Django ORM**: Database abstraction

### Message Broker
- **Redis 5.0.1**: Channel layer backend for WebSocket

### Frontend
- **Pure JavaScript**: No framework dependencies
- **WebSocket API**: Native browser WebSocket
- **Fetch API**: HTTP requests

## Key Components

### 1. Models (`user_app/models.py`)
```python
class User(models.Model):
    first_name = CharField
    last_name = CharField
    created_at = DateTimeField
    updated_at = DateTimeField
```

### 2. Serializers (`user_app/serializers.py`)
```python
class UserSerializer(ModelSerializer):
    - Validates incoming data
    - Converts to/from JSON
    - Handles partial updates (PATCH)
```

### 3. Views (`user_app/views.py`)
```python
@api_view(['PATCH'])
def user_detail(request, pk):
    - Receives PATCH request
    - Updates database
    - Broadcasts via WebSocket
    - Returns JSON response
```

### 4. WebSocket Consumer (`user_app/consumers.py`)
```python
class UserUpdateConsumer(AsyncWebsocketConsumer):
    - Handles WebSocket connections
    - Manages group membership
    - Broadcasts messages to group
```

### 5. Channel Layers (`settings.py`)
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {"hosts": [('127.0.0.1', 6379)]},
    },
}
```

## API Endpoints

### REST API

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/users/` | List all users | - |
| POST | `/api/users/` | Create user | `{first_name, last_name}` |
| GET | `/api/users/<id>/` | Get user | - |
| PATCH | `/api/users/<id>/` | Update user | `{first_name}` or `{last_name}` |
| DELETE | `/api/users/<id>/` | Delete user | - |

### WebSocket

| Protocol | Endpoint | Description |
|----------|----------|-------------|
| WS | `/ws/user-updates/` | Real-time updates |

## WebSocket Message Format

### Server → Client (Broadcast)
```json
{
  "type": "user_update",
  "data": {
    "action": "update",
    "user": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-01-13T10:00:00Z",
      "updated_at": "2026-01-13T10:05:00Z"
    }
  }
}
```

### Actions
- `update`: User data changed
- `create`: New user created
- `delete`: User deleted

## Security Considerations

### Current Implementation (POC)
- ❌ No authentication
- ❌ No authorization
- ❌ CSRF disabled for API
- ❌ CORS not configured
- ❌ No rate limiting

### Production Requirements
- ✓ Add Django authentication
- ✓ JWT tokens for API
- ✓ WebSocket authentication
- ✓ CSRF protection
- ✓ CORS configuration
- ✓ Rate limiting
- ✓ Input validation
- ✓ SQL injection protection (ORM handles this)
- ✓ XSS protection
- ✓ HTTPS/WSS only

## Scalability Considerations

### Current Limitations
- Single Django process
- Local Redis instance
- SQLite database (file-based)
- No load balancing

### Production Scaling
1. **Horizontal Scaling**
   - Multiple Django/Daphne workers
   - Load balancer (Nginx/HAProxy)
   - Redis cluster or Redis Sentinel

2. **Database**
   - PostgreSQL with connection pooling
   - Read replicas
   - Database indexes on frequently queried fields

3. **Caching**
   - Django cache framework
   - Redis for session storage
   - CDN for static files

4. **WebSocket Optimization**
   - Sticky sessions for WebSocket
   - WebSocket connection pooling
   - Message queue for heavy processing

## Performance Metrics

### Expected Performance (POC)
- API Response Time: < 50ms
- WebSocket Latency: < 100ms
- Database Query Time: < 10ms
- Concurrent Users: ~100
- Messages/second: ~1000

### Monitoring Points
- WebSocket connection count
- Active channel groups
- Redis memory usage
- Database query performance
- API endpoint response times

## Error Handling

### Client-Side
- WebSocket disconnection → Auto-reconnect (3s delay)
- API failure → Console error log
- Network error → Retry mechanism needed (future)

### Server-Side
- Invalid data → HTTP 400 with error details
- Not found → HTTP 404
- Server error → HTTP 500
- WebSocket error → Disconnect and log

## Testing Strategy

### Unit Tests
- Model validation
- Serializer validation
- View logic

### Integration Tests
- API endpoints
- WebSocket consumer
- Database transactions

### End-to-End Tests
- Full user flow
- Multi-window sync
- Real-time updates

### Load Tests
- Concurrent connections
- Message throughput
- Database performance

## Deployment Architecture (Production)

```
Internet
   │
   ▼
[Load Balancer - Nginx]
   │
   ├─> [Django/Daphne Worker 1] ──┐
   ├─> [Django/Daphne Worker 2] ──┼─> [PostgreSQL Primary]
   └─> [Django/Daphne Worker 3] ──┘         │
                │                            ├─> [PostgreSQL Replica]
                │                            └─> [PostgreSQL Replica]
                ▼
         [Redis Cluster]
         (Channel Layer)
                │
                ▼
       [Redis Sentinel]
       (High Availability)
```

## Future Enhancements

1. **Features**
   - User authentication
   - Field-level permissions
   - Conflict resolution
   - Undo/Redo functionality
   - Real-time typing indicators
   - Presence detection (who's online)

2. **Technical**
   - Add GraphQL subscriptions
   - Implement optimistic UI updates
   - Add offline support (Service Workers)
   - Implement delta sync (only send changes)
   - Add message compression

3. **DevOps**
   - Docker containerization
   - Kubernetes orchestration
   - CI/CD pipeline
   - Automated testing
   - Monitoring and alerting
   - Log aggregation

## References

- Django Channels: https://channels.readthedocs.io/
- Django REST Framework: https://www.django-rest-framework.org/
- WebSocket Protocol: https://datatracker.ietf.org/doc/html/rfc6455
- Redis: https://redis.io/documentation

---

**Document Version**: 1.0
**Last Updated**: 2026-01-13
**Author**: POC Development Team

