from django.urls import re_path as path

from channels.routing import ProtocolTypeRouter, URLRouter

from common.consumers import ChatConsumer
from common.routing import urlpatterns as common_routing

from .consumers import NotFoundConsumer


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        # WS v1
        path(
            r'^ws/v1/',
            URLRouter(common_routing)
        ),
        path(
            r'^',
            NotFoundConsumer,
            name='not-found-consumer'
        ),
    ])
})
