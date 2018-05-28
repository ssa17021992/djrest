from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import AsyncToSync


class Consumer(WebsocketConsumer):
    """Websocket consumer"""

    @property
    def kwargs(self):
        return self.scope['url_route']['kwargs']

    def group_add(self, name, channel_name):
        AsyncToSync(self.channel_layer.group_add)(name, channel_name)

    def group_send(self, name, content):
        AsyncToSync(self.channel_layer.group_send)(name, content)

    def group_discard(self, name, channel_name):
        AsyncToSync(self.channel_layer.group_discard)(name, channel_name)


class ChatConsumer(Consumer):
    """Chat consumer"""

    @property
    def chat_name(self):
        return 'chat-%s' % self.kwargs['room_id']

    def connect(self):
        self.accept()
        self.group_add(self.chat_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        self.group_send(self.chat_name, {
            'type': 'chat.message',
            'text': text_data
        })

    def chat_message(self, event):
        self.send(text_data=event['text'])

    def disconnect(self, close_code):
        self.group_discard(self.chat_name, self.channel_name)
