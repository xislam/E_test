import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Подключение к группе
        await self.channel_layer.group_add(
            'notification_group',
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Отключение от группы
        await self.channel_layer.group_discard(
            'notification_group',
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Обработка полученного сообщения
        print(f"Received message: {message}")

        # Отправка обратно клиенту
        await self.send(text_data=json.dumps({
            'message': 'Message received and processed successfully!',
        }))

        # Отправка уведомления всем подключенным клиентам
        await self.channel_layer.group_send(
            'notification_group',
            {
                'type': 'send_notification',
                'message': 'New product added/updated/deleted!',
            }
        )

    async def send_notification(self, event):
        # Отправка уведомления клиенту
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
