# Django WebSocket POC - Electron + Svelte Frontend

This is the **Electron + Svelte** frontend for the Django WebSocket POC. It connects to the Django backend for real-time data synchronization between two windows.

## 🎯 What This Does

**Window 1 (Purple):**
- ✏️ Edit **First Name** (editable)
- 👁️ View **Last Name** (read-only, synced from Window 2)

**Window 2 (Pink):**
- 👁️ View **First Name** (read-only, synced from Window 1)
- ✏️ Edit **Last Name** (editable)

**Real-time Magic:** Changes in one window instantly appear in the other via WebSocket! ⚡

## 🚀 Quick Start

### Prerequisites

1. **Node.js** 18+ installed
2. **Django backend** running on `http://localhost:8000`

### Installation

```bash
# Navigate to electron app directory
cd poc_websocket_electron

# Install dependencies
npm install
```

### Development Mode

```bash
# Run in development mode (opens both windows automatically)
npm run electron:dev
```

This will:
1. Start Vite dev server on `http://localhost:5173`
2. Launch Electron with two windows
3. Enable hot module replacement (HMR)
4. Open DevTools in both windows

### Manual Development

```bash
# Terminal 1: Start Vite dev server
npm run dev

# Terminal 2: Start Electron
npm run electron
```

## 📁 Project Structure

```
poc_websocket_electron/
├── electron/
│   ├── main.cjs           # Electron main process
│   └── preload.cjs        # Preload script
├── src/
│   ├── components/
│   │   ├── Window1.svelte # Window 1 component
│   │   └── Window2.svelte # Window 2 component
│   ├── services/
│   │   ├── api.js         # Django API service
│   │   └── websocket.js   # WebSocket service
│   ├── App.svelte         # Root component
│   ├── main.js            # Entry point
│   └── app.css            # Global styles
├── index.html             # HTML template
├── package.json           # Dependencies
├── vite.config.js         # Vite configuration
└── svelte.config.js       # Svelte configuration
```

## 🔧 Configuration

### Backend URLs

Update these in the service files if your Django backend is on a different host:

**`src/services/api.js`:**
```javascript
const DJANGO_API_URL = 'http://localhost:8000/api';
```

**`src/services/websocket.js`:**
```javascript
const DJANGO_WS_URL = 'ws://localhost:8000/ws/user-updates/';
```

## 📡 API Integration

### REST API (HTTP)

The app uses these Django endpoints:

```javascript
// GET /api/users/ - List all users
apiService.getUsers()

// GET /api/users/:id/ - Get user details
apiService.getUser(id)

// POST /api/users/ - Create user
apiService.createUser({ first_name, last_name })

// PATCH /api/users/:id/ - Update user (partial)
apiService.updateUser(id, { first_name: "New" })

// DELETE /api/users/:id/ - Delete user
apiService.deleteUser(id)
```

### WebSocket (Real-time)

Connection: `ws://localhost:8000/ws/user-updates/`

**Message Format (Server → Client):**
```json
{
  "type": "user_update",
  "data": {
    "action": "update",
    "user": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe"
    }
  }
}
```

## 🧪 Testing

### Manual Testing

1. Start Django backend:
   ```bash
   cd ../poc_websocket
   python manage.py runserver
   ```

2. Start Electron app:
   ```bash
   cd ../poc_websocket_electron
   npm run electron:dev
   ```

3. Test scenarios:
   - Edit First Name in Window 1 → Check Window 2
   - Edit Last Name in Window 2 → Check Window 1
   - Create user in either window → Appears in both
   - Stop Django → Connection status turns red
   - Restart Django → Auto-reconnects

## 🐛 Troubleshooting

### "Cannot connect to WebSocket"

**Problem:** Django backend not running or wrong URL

**Solution:**
- Ensure Django is running: `python manage.py runserver`
- Check WebSocket URL in `src/services/websocket.js`
- Verify Django has CORS headers enabled

### "API requests fail"

**Problem:** Django not configured for CORS

**Solution:**
- Install: `pip install django-cors-headers`
- Check Django settings.py has `corsheaders` in INSTALLED_APPS
- Check CORS_ALLOW_ALL_ORIGINS is set

### "Electron window is blank"

**Problem:** Vite dev server not running

**Solution:**
- Run `npm run dev` first
- Wait for "Local: http://localhost:5173"
- Then run `npm run electron`

## 📦 Building Executables

### Windows

```bash
npm run electron:build
```

Output: `dist-electron/` folder with `.exe` file

## 🎉 Features

✅ Two synchronized windows
✅ Real-time WebSocket updates
✅ PATCH API for database updates
✅ Auto-reconnection on disconnect
✅ Connection status indicators
✅ Beautiful gradient UI
✅ Editable/Read-only field management
✅ Create new users from both windows
✅ Hot module replacement (HMR)
✅ Cross-platform (Windows, Linux, macOS)

---

**Ready to code?** Run `npm run electron:dev` and start building! 🚀
