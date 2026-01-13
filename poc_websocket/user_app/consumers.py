import json
from channels.generic.websocket import AsyncWebsocketConsumer


class UserUpdateConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time user updates"""
    
    async def connect(self):
        # Join the user updates group
        self.room_group_name = 'user_updates'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave the user updates group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'user_update')
        data = text_data_json.get('data', {})
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_update',
                'data': data
            }
        )
    
    async def user_update(self, event):
        """Receive message from room group"""
        data = event['data']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_update',
            'data': data
        }))

