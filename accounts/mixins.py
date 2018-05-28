from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers
from rest_framework import status

from common.utils import get_object_or_none
from common import errors

from .models import User, SignUpCode, SocialLogin
from .clients import FacebookClient


class SignUpCodeMixin:
    """Sign up code mixin"""

    def delete_sign_up_codes(self, email):
        SignUpCode.objects.filter(Q(
            Q(email=email) | Q(expired__lt=timezone.now())
        )).delete()


class SocialSignInMixin:
    """Social sign in mixin"""

    def __validate_facebook_status_code(self, status_code, content):
        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            raise serializers.ValidationError({
              'connection': errors.FACEBOOK_API_CONNECTION_ERROR
            })

        if status_code != status.HTTP_200_OK:
            raise serializers.ValidationError({
                'token': content
            })

    def __validate_facebook_required_fields(self, attrs, required_fields, fields):
        if set(required_fields) != set(fields):
            raise serializers.ValidationError({
                'token': _('Invalid %(social)s fields "%(facebook_fields)s", must be "%(fields)s".') % {
                    'social': attrs['social'],
                    'facebook_fields': ', '.join(fields),
                    'fields': ', '.join(required_fields)
                }
            })

    def __validate_user_and_social_login(self, attrs, data):
        social_login = get_object_or_none(
            SocialLogin, social=attrs['social'],
            user__username=data['email']
        )
        user = get_object_or_none(User, username=data['email'])

        if not social_login and user:
            raise serializers.ValidationError({
                'username': errors.USERNAME_ALREADY_IN_USE
            })

        return (user, social_login)

    def __create_social_login(self, attrs, data):
        return SocialLogin.objects.create(
            social=attrs['social'],
            user=User.objects.create(**data)
        )

    def __get_facebook_social_login(self, attrs, data):
        user, social_login = self.__validate_user_and_social_login(attrs, data)

        if not social_login:
            f_birthday = data['birthday'].split('/')

            social_login = self.__create_social_login(attrs, {
                'firstName': data['first_name'],
                'middleName': data['middle_name'],
                'lastName': data['last_name'],
                'username': data['email'],
                'email': data['email'],
                'password': attrs['token'],
                'birthday': '{}-{}-{}'.format(
                    f_birthday[2], f_birthday[0], f_birthday[1] # yyyy-mm-dd format
                )
            })

        return social_login

    def login_with_facebook(self, attrs):
        fields = ('id', 'name', 'first_name',
            'middle_name', 'last_name', 'email', 'birthday')

        client = FacebookClient(access_token=attrs['token'])
        response = client.me()

        self.__validate_facebook_status_code(
            response.status,
            response.text if hasattr(response, 'text') else ''
        )

        data = response.json()
        self.__validate_facebook_required_fields(
            attrs,
            fields,
            data.keys()
        )

        return self.__get_facebook_social_login(attrs, data)
