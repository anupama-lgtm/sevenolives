# Testing Guide - Django WebSocket POC

## Quick Start Testing

### Method 1: Using Helper Scripts (Recommended)

**Windows:**
```bash
cd poc_websocket
start_project.bat
```

**Linux/Mac:**
```bash
cd poc_websocket
chmod +x start_project.sh
./start_project.sh
```

### Method 2: Manual Setup

1. **Start Redis** (in Terminal 1):
```bash
redis-server
```

2. **Check Redis Connection** (Optional):
```bash
python check_redis.py
```

3. **Start Django Server** (in Terminal 2):
```bash
cd poc_websocket
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate, Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python create_sample_data.py  # Create sample users
python manage.py runserver
```

## Test Scenarios

### Test 1: Basic Real-time Sync

1. Open **Window 1**: http://localhost:8000/window1/
2. Open **Window 2**: http://localhost:8000/window2/
3. Verify WebSocket connection (should show green "🟢 Connected")

**Test Steps:**
- In Window 1: Change "John" → "Johnny" (First Name)
- Check Window 2: First Name should update to "Johnny" automatically
- In Window 2: Change "Doe" → "Doe Jr." (Last Name)  
- Check Window 1: Last Name should update to "Doe Jr." automatically

**Expected Result:** ✓ Both windows sync in real-time

---

### Test 2: Multiple User Updates

1. Create multiple users in Window 1 or 2
2. Edit different users' fields
3. Verify all changes sync across both windows

**Test Steps:**
- Window 1: Edit First Name of User 1
- Window 2: Edit Last Name of User 2
- Window 1: Edit First Name of User 3
- Verify all changes appear in both windows

**Expected Result:** ✓ All updates sync correctly

---

### Test 3: Create New User

**Test Steps:**
1. In Window 1, fill the "Create New User" form:
   - First Name: "Test"
   - Last Name: "User"
2. Click "Create User"
3. Check both windows

**Expected Result:** 
- ✓ New user appears in both windows instantly
- ✓ Window 1: First Name is editable, Last Name is read-only
- ✓ Window 2: Last Name is editable, First Name is read-only

---

### Test 4: Read-only Enforcement

**Test Steps:**
1. In Window 1: Try to click on Last Name field
2. In Window 2: Try to click on First Name field

**Expected Result:** 
- ✓ Fields are grayed out
- ✓ Cannot edit read-only fields
- ✓ Cursor shows "not-allowed" icon

---

### Test 5: WebSocket Reconnection

**Test Steps:**
1. Open both windows (verify green connection status)
2. Stop Redis server (Ctrl+C in Redis terminal)
3. Watch connection status turn red: "🔴 WebSocket Disconnected"
4. Restart Redis server: `redis-server`
5. Wait 3 seconds

**Expected Result:** 
- ✓ Connection automatically reconnects
- ✓ Status turns green again
- ✓ Updates continue to sync

---

### Test 6: Multiple Browser Windows

**Test Steps:**
1. Open Window 1 in Chrome
2. Open Window 2 in Chrome
3. Open Window 1 in Firefox
4. Open Window 2 in Firefox
5. Make changes in any window

**Expected Result:** 
- ✓ All 4 windows update simultaneously
- ✓ Changes propagate to all connected clients

---

### Test 7: PATCH API Direct Testing

**Test with cURL/Postman:**

```bash
# Get all users
curl http://localhost:8000/api/users/

# Get specific user
curl http://localhost:8000/api/users/1/

# Update first name only (PATCH)
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "UpdatedName"}'

# Update last name only (PATCH)
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"last_name": "UpdatedLastName"}'

# Create new user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "API", "last_name": "User"}'
```

**Expected Result:** 
- ✓ API calls succeed
- ✓ Changes appear in both windows in real-time
- ✓ Database is updated

---

### Test 8: Browser Console Inspection

**Test Steps:**
1. Open both windows
2. Open browser DevTools (F12)
3. Go to Console tab
4. Make changes in fields
5. Observe console logs

**Expected Logs:**
```
WebSocket connected
WebSocket message received: {type: "user_update", data: {...}}
User updated: {id: 1, first_name: "...", last_name: "..."}
```

**Expected Result:** ✓ All WebSocket events are logged

---

### Test 9: Network Tab Inspection

**Test Steps:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Filter by "WS" (WebSocket)
4. Make changes in fields

**Expected Result:** 
- ✓ WebSocket connection visible
- ✓ Messages visible in Frames tab
- ✓ PATCH requests visible with correct payloads

---

### Test 10: Database Persistence

**Test Steps:**
1. Make changes in both windows
2. Stop Django server (Ctrl+C)
3. Restart Django server: `python manage.py runserver`
4. Refresh both windows

**Expected Result:** 
- ✓ All changes are persisted
- ✓ Data loads from database
- ✓ No data loss

---

## Performance Testing

### Test 11: Rapid Updates

**Test Steps:**
1. Rapidly type in First Name field in Window 1
2. Observe Window 2 updates

**Expected Result:** 
- ✓ Updates are smooth
- ✓ No lag or delay
- ✓ Final value is correct

---

### Test 12: Concurrent Updates

**Test Steps:**
1. Open Window 1 and Window 2 side by side
2. Simultaneously:
   - Type in First Name (Window 1)
   - Type in Last Name (Window 2)

**Expected Result:** 
- ✓ No conflicts
- ✓ Both updates are saved
- ✓ Both windows show correct final values

---

## Error Handling Testing

### Test 13: Empty Values

**Test Steps:**
1. Clear First Name field completely
2. Click outside (trigger onChange)
3. Clear Last Name field completely

**Expected Result:** 
- ✓ Empty values are accepted
- ✓ Updates sync correctly
- ✓ No errors

---

### Test 14: Special Characters

**Test Steps:**
1. Enter: `Jöhn O'Brien-Smith`
2. Enter: `José María García`
3. Enter: `李明 (Li Ming)`

**Expected Result:** 
- ✓ Special characters handled correctly
- ✓ Unicode support works
- ✓ No encoding issues

---

## Troubleshooting Tests

### If Real-time Sync Doesn't Work:

1. **Check Redis:**
   ```bash
   python check_redis.py
   ```
   Should show: ✓ Redis is running

2. **Check WebSocket Connection:**
   - Look for green status in UI
   - Check browser console for errors

3. **Check Django Server:**
   - Ensure running with Daphne (ASGI)
   - Check terminal for errors

4. **Check CORS/Network:**
   - Ensure using localhost (not 127.0.0.1 vs localhost)
   - Check firewall settings

---

## Success Criteria

✓ All tests pass
✓ Real-time sync works consistently
✓ No console errors
✓ WebSocket stays connected
✓ Database updates persist
✓ UI is responsive and intuitive
✓ Read-only fields cannot be edited
✓ Multiple windows sync correctly

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| WebSocket won't connect | Start Redis server |
| Changes don't sync | Refresh page, check WebSocket status |
| Redis connection error | Run `redis-server` in separate terminal |
| Import errors | Run `pip install -r requirements.txt` |
| Database errors | Run `python manage.py migrate` |
| Port 8000 in use | Change port: `python manage.py runserver 8080` |

---

## Demo Script

**For demonstrating to others:**

1. "Let me show you the two windows..." (Open both)
2. "Notice Window 1 can edit First Name, Window 2 can edit Last Name"
3. "Watch what happens when I change this..." (Edit First Name in Window 1)
4. "See? It updates in Window 2 immediately!"
5. "Now let me edit Last Name in Window 2..." (Edit)
6. "And it updates in Window 1 instantly!"
7. "This is using WebSockets for real-time communication"
8. "The backend is Django with Channels, database is SQLite"
9. "And we're using PATCH API calls for partial updates"

---

## Video Recording Checklist

If recording a demo:
- [ ] Show both windows side by side
- [ ] Demonstrate First Name edit → Window 2 update
- [ ] Demonstrate Last Name edit → Window 1 update  
- [ ] Show WebSocket connection status
- [ ] Show browser console with messages
- [ ] Show Network tab with WebSocket frames
- [ ] Create a new user from both windows
- [ ] Show that changes persist after refresh

---

## Next Steps After Testing

- [ ] Add authentication/authorization
- [ ] Add field validation
- [ ] Add delete functionality in UI
- [ ] Add user search/filter
- [ ] Add timestamps display
- [ ] Add conflict resolution
- [ ] Add offline support
- [ ] Deploy to production server

Happy Testing! 🚀

