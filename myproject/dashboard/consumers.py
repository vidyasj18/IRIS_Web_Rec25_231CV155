import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AdminDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_dashboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_dashboard", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        
        # Broadcast the action to all admin clients
        await self.channel_layer.group_send(
            "admin_dashboard",
            {
                "type": "update_admin_dashboard",
                "action": action,
                "message": data.get("message"),
            }
        )

    async def update_admin_dashboard(self, event):
        await self.send(text_data=json.dumps({
            "action": event["action"],
            "message": event["message"],
        }))
