from django.utils import timezone
from rest_framework import serializers
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync

from common.mixins import QueryFieldsMixin

from .utils import to_object
from .tasks import send_fcm_notification, send_mail


class FruitListSerializer(QueryFieldsMixin, serializers.Serializer):
    """Fruit list serializer"""

    id = serializers.CharField(max_length=22)
    name = serializers.CharField(max_length=50)


class LocalTimeSerializer(serializers.Serializer):
    """Local time serializer"""

    localTime = serializers.DateTimeField()


class FCMSerializer(serializers.Serializer):
    """FCM serializer"""

    title = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=150)

    to = serializers.CharField(max_length=200)

    def create(self, validated_data):
        send_fcm_notification.delay(
            title=validated_data['title'],
            body=validated_data['body'],
            to=[validated_data['to']]
        )
        return to_object(validated_data)


class MailSerializer(serializers.Serializer):
    """Mail serializer"""

    subject = serializers.CharField(max_length=120)
    body = serializers.CharField(max_length=150)

    to = serializers.EmailField()

    def create(self, validated_data):
        send_mail.delay(**validated_data)
        return to_object(validated_data)


class MsgSerializer(serializers.Serializer):
    """Message serializer"""

    room = serializers.CharField(max_length=40)
    content = serializers.CharField(max_length=250)

    def create(self, validated_data):
        room = validated_data['room']
        content = validated_data['content']

        channel_layer = get_channel_layer()

        group_send = AsyncToSync(channel_layer.group_send)
        group_send(room, {
            'type': 'chat.message',
            'text': content
        })
        return to_object(validated_data)
