from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.send_notification('Новый пользователь добавлен!')
        return response

    def send_notification(self, message):
        channel_layer = get_channel_layer()

        async def send():
            await channel_layer.group_send(
                'notification_group',
                {
                    'type': 'send_notification',
                    'message': message,
                }
            )

        async_to_sync(send)()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.send_notification('Пользователь обновлен!')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.send_notification('Пользователь удален!')
        return response

    def send_notification(self, message):
        channel_layer = get_channel_layer()

        async def send():
            await channel_layer.group_send(
                'notification_group',
                {
                    'type': 'send_notification',
                    'message': message,
                }
            )

        async_to_sync(send)()
