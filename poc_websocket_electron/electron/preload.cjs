// Preload script for Electron
// Exposes safe APIs to renderer process

const { contextBridge } = require('electron');

// Expose protected methods that allow the renderer process to use
// the electron APIs without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
  // Add more APIs as needed
});

// Expose a safe subset of environment variables to the renderer.
// Only variables prefixed with RENDERER_ will be forwarded.
const safeEnv = Object.fromEntries(
  Object.entries(process.env).filter(([key]) => key.startsWith('RENDERER_'))
);

contextBridge.exposeInMainWorld('env', safeEnv);
