from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.send_notification('New Product added!')
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


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        # Логика обновления объекта Product

        # Отправка уведомления
        self.send_notification('Product updated!')

        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Логика удаления объекта Product

        # Отправка уведомления
        self.send_notification('Product removed!')

        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

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
