from django.urls import re_path as path

from .consumers import ChatConsumer


urlpatterns = [
    path(
        r'^common/rooms/(?P<room_id>[0-9]{1,20})$',
        ChatConsumer,
        name='chat-consumer'
    ),
]
