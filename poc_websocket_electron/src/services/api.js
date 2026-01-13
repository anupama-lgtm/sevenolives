// API service for Django backend
const DJANGO_API_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseUrl = DJANGO_API_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // Handle empty responses (like DELETE)
      if (response.status === 204) {
        return null;
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Get all users
  async getUsers() {
    return this.request('/users/');
  }

  // Get single user
  async getUser(id) {
    return this.request(`/users/${id}/`);
  }

  // Create user
  async createUser(userData) {
    return this.request('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Update user (PATCH - partial update)
  async updateUser(id, userData) {
    return this.request(`/users/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(userData),
    });
  }

  // Delete user
  async deleteUser(id) {
    return this.request(`/users/${id}/`, {
      method: 'DELETE',
    });
  }
}

export const apiService = new ApiService();
