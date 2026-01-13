<script>
  import { onMount, onDestroy } from 'svelte';
  import { wsService } from '../services/websocket.js';
  import { apiService } from '../services/api.js';

  let users = [];
  let newFirstName = '';
  let newLastName = '';
  let isConnected = false;
  let unsubscribe;
  // Debounce timers per (userId, field)
  let updateTimers = new Map();

  onMount(async () => {
    // Connect to WebSocket
    wsService.connect();

    // Subscribe to WebSocket messages
    unsubscribe = wsService.subscribe(handleWebSocketMessage);

    // Load initial users
    await loadUsers();
  });

  onDestroy(() => {
    if (unsubscribe) {
      unsubscribe();
    }
  });

  async function loadUsers() {
    try {
      users = await apiService.getUsers();
    } catch (error) {
      console.error('Failed to load users:', error);
    }
  }

  function handleWebSocketMessage(data) {
    if (data.type === 'connection_status') {
      isConnected = data.isConnected;
      return;
    }

    if (data.type === 'user_update') {
      const { action, user, user_id } = data.data;

      if (action === 'update') {
        // Update existing user
        users = users.map(u => u.id === user.id ? user : u);
      } else if (action === 'create') {
        // Add new user
        if (!users.find(u => u.id === user.id)) {
          users = [...users, user];
        }
      } else if (action === 'delete') {
        // Remove user
        users = users.filter(u => u.id !== user_id);
      }
    }
  }

  // Optimistically update local state so the read-only mirror updates instantly
  function applyLocalUpdate(userId, field, value) {
    users = users.map(u => (u.id === userId ? { ...u, [field]: value } : u));
  }

  // Debounced API update to reduce requests while typing
  async function scheduleUpdate(userId, field, value) {
    applyLocalUpdate(userId, field, value);

    const key = `${userId}:${field}`;
    const existing = updateTimers.get(key);
    if (existing) clearTimeout(existing);

    const timer = setTimeout(async () => {
      try {
        await apiService.updateUser(userId, { [field]: value });
        console.log(`Updated user ${userId}: ${field} = ${value}`);
      } catch (error) {
        console.error('Failed to update user:', error);
      } finally {
        updateTimers.delete(key);
      }
    }, 300);

    updateTimers.set(key, timer);
  }

  async function createUser() {
    if (!newFirstName && !newLastName) {
      alert('Please enter at least one name');
      return;
    }

    try {
      await apiService.createUser({
        first_name: newFirstName,
        last_name: newLastName
      });
      newFirstName = '';
      newLastName = '';
    } catch (error) {
      console.error('Failed to create user:', error);
      alert('Failed to create user');
    }
  }
</script>

<div class="container window2-bg">
  <div class="content window2">
    <h1>Window 2 <span class="badge">Edit Last Name</span></h1>
    <p class="subtitle">You can edit Last Name here. First Name is synced from Window 1 (Read-only)</p>
    
    <div class="connection-status {isConnected ? 'connected' : 'disconnected'}">
      {isConnected ? '🟢 Connected to WebSocket' : '🔴 Connecting to WebSocket...'}
    </div>
    
    <div class="create-section">
      <h3>➕ Create New User</h3>
      <div class="form-group">
        <label>First Name:</label>
        <input type="text" bind:value={newFirstName} placeholder="Enter first name">
      </div>
      <div class="form-group">
        <label>Last Name:</label>
        <input type="text" bind:value={newLastName} placeholder="Enter last name">
      </div>
      <button class="btn" on:click={createUser}>Create User</button>
    </div>
    
    <div class="users-list">
      {#if users.length === 0}
        <div class="no-users">
          No users found. Create a new user above!
        </div>
      {:else}
        {#each users as user (user.id)}
          <div class="user-card">
            <div class="user-id">User ID: {user.id}</div>
            <div class="form-group">
              <label>First Name: <span class="badge read-only">Read Only</span></label>
              <input 
                type="text" 
                value={user.first_name || ''}
                readonly
              >
            </div>
            <div class="form-group">
              <label>Last Name: <span class="badge">Editable</span></label>
              <input 
                type="text" 
                value={user.last_name || ''}
                on:input={(e) => scheduleUpdate(user.id, 'last_name', e.target.value)}
              >
            </div>
          </div>
        {/each}
      {/if}
    </div>
  </div>
</div>
