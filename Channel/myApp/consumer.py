from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .models import Chat, Group
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json

class myAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print("Connection Established...")
        # print("Channel Layer: ", self.channel_layer)
        # print("Channel Name: ", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        self.group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({
                    'type': 'websocket.accept'
                })
    
    async def websocket_receive(self, event):
        # print("Message Received...", event)
        json_data = json.loads(event['text'])
        self.chat = await sync_to_async(Chat)(message=json_data['text'], user=json_data['user'], group=self.group)
        await sync_to_async(self.chat.save)()
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'message': event['text']
        })
        
    async def chat_message(self, event):
        # print("Event...", event)
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        # print("Websocket Disconnected...")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()