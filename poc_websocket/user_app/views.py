from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import User
from .serializers import UserSerializer


def window1_view(request):
    """Render Window 1 - Editable first_name, readonly last_name"""
    users = User.objects.all()
    return render(request, 'window1.html', {'users': users})


def window2_view(request):
    """Render Window 2 - Readonly first_name, editable last_name"""
    users = User.objects.all()
    return render(request, 'window2.html', {'users': users})


@api_view(['GET', 'POST'])
def user_list(request):
    """List all users or create a new user"""
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Broadcast update via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'user_updates',
                {
                    'type': 'user_update',
                    'data': {
                        'action': 'create',
                        'user': UserSerializer(user).data
                    }
                }
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def user_detail(request, pk):
    """Retrieve, update or delete a user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            
            # Broadcast update via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'user_updates',
                {
                    'type': 'user_update',
                    'data': {
                        'action': 'update',
                        'user': UserSerializer(user).data
                    }
                }
            )
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user_id = user.id
        user.delete()
        
        # Broadcast delete via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'user_updates',
            {
                'type': 'user_update',
                'data': {
                    'action': 'delete',
                    'user_id': user_id
                }
            }
        )
        
        return Response(status=status.HTTP_204_NO_CONTENT)

