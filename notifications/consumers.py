import codecs
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'join_group':
            # Присоединяем клиента к группе
            await self.channel_layer.group_add('notification_group', self.channel_name)
            print(f"Client {self.channel_name} joined 'notification_group'")

    async def disconnect(self, close_code):
        # Удаляем клиента из группы при отключении
        await self.channel_layer.group_discard('notification_group', self.channel_name)
        print(f"Client {self.channel_name} left 'notification_group'")

    async def send_notification(self, event):
        # Декодируем Unicode escape sequences в UTF-8
        decoded_message = codecs.decode(event['message'], 'unicode_escape').encode('latin1').decode('utf-8')
        print(decoded_message)
        # Отправка уведомления всем подключенным клиентам в группе 'notification_group'
        await self.send(text_data=json.dumps({
            'message': decoded_message,
        }))