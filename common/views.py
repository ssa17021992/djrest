from django.views.static import serve
from django.utils import timezone
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status

from accounts.permissions import AllowAny

from .generics import CreateWithStatusAPIView
from .response import Response
from .pagination import PageNumberPagination
from .utils import to_object, unique_id
from .serializers import (
    FruitListSerializer,
    LocalTimeSerializer,
    FCMSerializer,
    MailSerializer,
    MsgSerializer,
)


class FruitAPIView(APIView):
    """Fruit api view"""

    pagination_class = PageNumberPagination
    queryset = []
    serializer_class = FruitListSerializer

    def __init__(self):
        self.paginator = self.pagination_class()

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)

    def get_queryset(self):
        self.queryset = [{
            'id': unique_id(),
            'name': 'Apple {0}'.format(i)
        } for i in range(1000)]

        return self.queryset

    def paginate_queryset(self, queryset):
        return self.paginator.paginate_queryset(
            queryset, self.request
        )

    def get(self, request):
        data = self.paginate_queryset(self.get_queryset())
        serializer = self.serializer_class(
            data,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class DateTimeAPIView(APIView):
    """Date time api view"""

    serializer_class = LocalTimeSerializer

    def get_object(self):
        return to_object({
            'localTime': timezone.now()
        })

    def get(self, request):
        """Get local time"""
        serializer = self.serializer_class(
            self.get_object(),
            many=False,
            context={'request': request}
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class ServeAPIView(APIView):
    """Serve api view"""

    permission_classes = (AllowAny,)

    def get(self, request, path):
        """Get file"""
        return serve(
            request,
            path,
            document_root=settings.MEDIA_ROOT
        )


class FCMAPIView(CreateWithStatusAPIView):
    """FCM api view"""

    serializer_class = FCMSerializer


class MailAPIView(CreateWithStatusAPIView):
    """Mail api view"""

    serializer_class = MailSerializer


class MsgAPIView(APIView):
    """Message api view"""

    serializer_class = MsgSerializer

    def post(self, request, room_id):
        """Send message to group"""
        data = request.data
        if isinstance(data, dict):
            data['room'] = 'chat-%s' % room_id

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(status=status.HTTP_200_OK)
