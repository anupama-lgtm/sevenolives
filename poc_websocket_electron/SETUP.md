# Quick Setup Guide - Electron + Svelte Frontend

## 🚀 3-Step Setup

### Step 1: Start Django Backend

```bash
# Terminal 1
cd poc_websocket
python manage.py runserver
```

Keep this running!

### Step 2: Install Dependencies

```bash
# Terminal 2
cd poc_websocket_electron
npm install
```

### Step 3: Run Electron App

```bash
npm run electron:dev
```

## ✨ What You'll See

Two Electron windows will open:

1. **Window 1 (Purple)** - Edit First Name
2. **Window 2 (Pink)** - Edit Last Name

## 🧪 Test It

1. Type in First Name (Window 1)
2. Watch it appear in Window 2 (read-only)
3. Type in Last Name (Window 2)  
4. Watch it appear in Window 1 (read-only)

## ✅ Success Indicators

- 🟢 Green "Connected to WebSocket" in both windows
- ⚡ Instant sync between windows
- 💾 Data persists after refresh

## 🐛 Quick Fixes

**Problem:** "Cannot connect"
**Fix:** Start Django backend first

**Problem:** "npm install fails"
**Fix:** Use Node.js 18+

**Problem:** Blank window
**Fix:** Wait for Vite server to start

---

**Need help?** Check the main README.md file!
