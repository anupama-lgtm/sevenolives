// WebSocket service for real-time communication with Django backend
const DJANGO_WS_URL = 'ws://localhost:8000/ws/user-updates/';

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectInterval = 3000;
    this.listeners = [];
    this.isConnected = false;
  }

  connect() {
    try {
      this.ws = new WebSocket(DJANGO_WS_URL);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.isConnected = true;
        this.notifyStatusChange(true);
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('WebSocket message received:', data);
        this.notifyListeners(data);
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.isConnected = false;
        this.notifyStatusChange(false);
        
        // Auto-reconnect after 3 seconds
        setTimeout(() => {
          console.log('Attempting to reconnect...');
          this.connect();
        }, this.reconnectInterval);
      };
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  // Subscribe to WebSocket messages
  subscribe(callback) {
    this.listeners.push(callback);
    
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  notifyListeners(data) {
    this.listeners.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error('Error in WebSocket listener:', error);
      }
    });
  }

  notifyStatusChange(isConnected) {
    this.listeners.forEach(callback => {
      try {
        callback({ type: 'connection_status', isConnected });
      } catch (error) {
        console.error('Error notifying status change:', error);
      }
    });
  }

  getConnectionStatus() {
    return this.isConnected;
  }
}

// Singleton instance
export const wsService = new WebSocketService();
