from django.utils.translation import gettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from common.response import Response
from common.generics import CreateWithStatusAPIView

from .authentication import PasswdTokenAuthentication
from .permissions import AllowAny
from .models import User
from .serializers import (
    SignUpAvailableSerializer,
    SignUpMailSerializer,
    SignUpCheckSerializer,
    SignUpSerializer,
    SignInSerializer,

    SocialSignInSerializer,

    ProfileSerializer,
    ProfilePartialUpdateSerializer,
    AvatarSerializer,

    ChangeSerializer,

    ResetMailSerializer,
    ResetSerializer,

    UserListSerializer,
)


class SignUpAvailableAPIView(CreateWithStatusAPIView):
    """Sign up available api view"""

    permission_classes = (AllowAny,)
    serializer_class = SignUpAvailableSerializer


class SignUpMailAPIView(CreateWithStatusAPIView):
    """Sign up mail api view"""

    permission_classes = (AllowAny,)
    serializer_class = SignUpMailSerializer


class SignUpCheckAPIView(CreateWithStatusAPIView):
    """Sign up check api view"""

    permission_classes = (AllowAny,)
    serializer_class = SignUpCheckSerializer


class SignUpAPIView(CreateWithStatusAPIView):
    """Sign up api view"""

    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    status_code = status.HTTP_201_CREATED


class SignInAPIView(APIView):
    """Sign in api view"""

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request):
        """Sign in user"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(data={
            'token': serializer.instance.token
        }, status=status.HTTP_200_OK)


class SocialSignInAPIView(SignInAPIView):
    """Social sign in api view"""

    serializer_class = SocialSignInSerializer


class ProfileAPIView(APIView):
    """Profile api view"""

    serializer_class = ProfileSerializer
    serializer_partial_update_class = ProfilePartialUpdateSerializer

    def get(self, request):
        """Get user profile"""
        serializer = self.serializer_class(
            request.user,
            context={'request': request}
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        serializer = self.serializer_partial_update_class(
            request.user,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AvatarAPIView(APIView):
    """Avatar api view"""

    parser_classes = (MultiPartParser,)
    serializer_class = AvatarSerializer

    def put(self, request):
        data = {}
        file = request.FILES.get('avatar')

        if file: data['avatar'] = file

        serializer = self.serializer_class(request.user, data=data)
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ChangeAPIView(APIView):
    """Password change api view"""

    serializer_class = ChangeSerializer

    def post(self, request):
        """Change password"""
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(status=status.HTTP_200_OK)


class ResetMailAPIView(CreateWithStatusAPIView):
    """Password reset mail api view"""

    permission_classes = (AllowAny,)
    serializer_class = ResetMailSerializer


class ResetCheckAPIView(APIView):
    """Password reset code check api view"""

    authentication_classes = (PasswdTokenAuthentication,)

    def post(self, request):
        """Verify if token is valid"""
        return Response(status=status.HTTP_200_OK)


class ResetAPIView(APIView):
    """Password reset api view"""

    authentication_classes = (PasswdTokenAuthentication,)
    serializer_class = ResetSerializer

    def post(self, request):
        """Reset password"""
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserAPIView(ListAPIView):
    """User api view"""

    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        return self.queryset.filter(isActive=True)
