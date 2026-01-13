// Preload script for Electron
// Exposes safe APIs to renderer process

const { contextBridge } = require('electron');

// Expose protected methods that allow the renderer process to use
// the electron APIs without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
  // Add more APIs as needed
});
