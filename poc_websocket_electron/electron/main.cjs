const { app, BrowserWindow } = require('electron');
const path = require('path');

let window1 = null;
let window2 = null;

function createWindow1() {
  window1 = new BrowserWindow({
    width: 900,
    height: 800,
    title: 'Window 1 - Edit First Name',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs')
    },
    backgroundColor: '#667eea',
    show: false
  });

  // Load from Vite dev server in development, or dist in production
  const isDev = process.env.NODE_ENV !== 'production';
  
  if (isDev) {
    window1.loadURL('http://localhost:5173/#/window1');
    window1.webContents.openDevTools();
  } else {
    window1.loadFile(path.join(__dirname, '../dist/index.html'), {
      hash: '/window1'
    });
  }

  window1.once('ready-to-show', () => {
    window1.show();
  });

  window1.on('closed', () => {
    window1 = null;
  });
}

function createWindow2() {
  window2 = new BrowserWindow({
    width: 900,
    height: 800,
    title: 'Window 2 - Edit Last Name',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs')
    },
    backgroundColor: '#f5576c',
    show: false
  });

  const isDev = process.env.NODE_ENV !== 'production';
  
  if (isDev) {
    window2.loadURL('http://localhost:5173/#/window2');
    window2.webContents.openDevTools();
  } else {
    window2.loadFile(path.join(__dirname, '../dist/index.html'), {
      hash: '/window2'
    });
  }

  window2.once('ready-to-show', () => {
    window2.show();
    
    // Position window2 next to window1
    if (window1) {
      const [x, y] = window1.getPosition();
      const [width] = window1.getSize();
      window2.setPosition(x + width + 10, y);
    }
  });

  window2.on('closed', () => {
    window2 = null;
  });
}

app.whenReady().then(() => {
  // Create both windows
  createWindow1();
  
  // Create window2 after a short delay
  setTimeout(() => {
    createWindow2();
  }, 500);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow1();
      setTimeout(createWindow2, 500);
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
