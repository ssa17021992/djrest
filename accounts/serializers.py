from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import (
    FileExtensionValidator, RegexValidator)
from rest_framework import serializers

from common.mixins import QueryFieldsMixin
from common.utils import get_object_or_none, to_object
from common import regex
from common import errors

from .auth import authenticate, auth_token, passwd_token
from .models import User, SignUpCode, SocialLogin
from .tasks import send_signup_mail, send_passwd_reset_mail
from .mixins import SignUpCodeMixin, SocialSignInMixin


class SignUpAvailableSerializer(serializers.Serializer):
    """Sign up available serializer"""

    username = serializers.CharField(max_length=200)

    def validate_username(self, value):
        user = get_object_or_none(User, username=value)
        if user:
            raise serializers.ValidationError(
                errors.USERNAME_ALREADY_IN_USE
            )
        return value

    def create(self, validated_data):
        return to_object(validated_data)


class SignUpMailSerializer(SignUpCodeMixin, serializers.ModelSerializer):
    """Sign up mail serializer"""

    def validate_email(self, value):
        codes = User.objects.filter(email=value)
        if codes.count() > settings.SIGNUP_EMAIL_USE_LIMIT:
            raise serializers.ValidationError(
                _('This email address has been used many times.')
            )
        return value

    def create(self, validated_data):
        self.delete_sign_up_codes(validated_data['email'])

        instance = super(self.__class__, self).create(validated_data)

        send_signup_mail.delay(instance.code, instance.email)
        return instance

    class Meta:
        model = SignUpCode
        exclude = ('code', 'expired')


class SignUpCheckSerializer(SignUpCodeMixin, serializers.Serializer):
    """Sign up check serializer"""

    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        obj = get_object_or_none(SignUpCode,
            email=attrs['email'], code=attrs['code'])
        if not obj:
            self.delete_sign_up_codes(attrs['email'])
            raise serializers.ValidationError({
                'code': errors.INVALID_SIGN_UP_CODE
            })

        if not obj.is_valid:
            obj.delete()  # Delete sign up code
            raise serializers.ValidationError({
                'code': errors.INVALID_SIGN_UP_CODE
            })
        return attrs

    def create(self, validated_data):
        return to_object(validated_data)


class SignUpSerializer(SignUpCodeMixin, serializers.ModelSerializer):
    """Sign up serializer"""

    password = serializers.CharField(max_length=200,
        validators=[RegexValidator(regex.PASSWORD)])

    code = serializers.CharField(max_length=4)

    def validate(self, attrs):
        obj = get_object_or_none(SignUpCode,
            email=attrs['email'], code=attrs['code'])
        if not obj:
            self.delete_sign_up_codes(attrs['email'])
            raise serializers.ValidationError({
                'code': errors.INVALID_SIGN_UP_CODE
            })

        if not obj.is_valid:
            obj.delete()  # Delete sign up code
            raise serializers.ValidationError({
                'code': errors.INVALID_SIGN_UP_CODE
            })

        self.context['code'] = obj
        return attrs

    def create(self, validated_data):
        self.context['code'].delete()  # Delete sign up code
        self.delete_sign_up_codes(validated_data['email'])

        validated_data.pop('code')

        instance = super(self.__class__, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        exclude = ('avatar', 'isActive', 'renewed')


class SignInSerializer(serializers.Serializer):
    """Sign in serializer"""

    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate_username(self, value):
        user = get_object_or_none(User, username=value)
        if not user:
            raise serializers.ValidationError(
                errors.USER_DOES_NOT_EXIST
            )

        if not user.isActive:
            raise serializers.ValidationError(
                errors.USER_INACTIVE
            )

        self.context['user'] = user
        return value

    def validate(self, attrs):
        user = authenticate(attrs['username'],
            attrs['password'], instance=self.context['user'])
        if not user:
            raise serializers.ValidationError({
                'password': errors.INCORRECT_PASSWORD
            })
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        user.token = auth_token(user)
        return user


class SocialSignInSerializer(SocialSignInMixin, serializers.Serializer):
    """Social sign in serializer"""

    social = serializers.CharField(max_length=10)
    token = serializers.CharField(max_length=300)

    def validate_social(self, value):
        socials = ('facebook',)
        if not value in socials:
            raise serializers.ValidationError(
                errors.SOCIAL_DOES_NOT_EXIST
            )
        return value

    def validate(self, attrs):
        if attrs['social'] == 'facebook':
            social_login = self.login_with_facebook(attrs)

        if not social_login.user.isActive:
            raise serializers.ValidationError({
                'username': errors.USER_INACTIVE
            })

        self.context['social_login'] = social_login
        return attrs

    def create(self, validated_data):
        user = self.context['social_login'].user
        user.token = auth_token(user)
        return user


class ProfileSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    """Profile serializer"""

    class Meta:
        model = User
        exclude = ('password', 'isActive', 'renewed')


class ProfilePartialUpdateSerializer(serializers.ModelSerializer):
    """Profile partial update serializer"""

    class Meta:
        model = User
        fields = ('firstName',
            'middleName', 'lastName', 'birthday')


class AvatarSerializer(serializers.ModelSerializer):
    """Avatar serializer"""

    class Meta:
        model = User
        fields = ('avatar',)
        extra_kwargs = {'avatar': {'required': True}}


class ChangeSerializer(serializers.Serializer):
    """Password change serializer"""

    current = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200,
        validators=[RegexValidator(regex.PASSWORD)])

    def validate_current(self, value):
        if not authenticate(self.instance.username,
            value, instance=self.instance):
            raise serializers.ValidationError(
                errors.INCORRECT_PASSWORD
            )
        return value

    def validate(self, attrs):
        if attrs['current'] == attrs['password']:
            raise serializers.ValidationError({
                'password': errors.SAME_PASSWORD
            })
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ResetMailSerializer(serializers.Serializer):
    """Password reset mail serializer"""

    username = serializers.CharField(max_length=200)

    def validate_username(self, value):
        user = get_object_or_none(User, username=value)
        if not user:
            raise serializers.ValidationError(
                errors.USER_DOES_NOT_EXIST
            )

        self.context['user'] = user
        return value

    def create(self, validated_data):
        user = self.context['user']
        token = passwd_token(user)

        send_passwd_reset_mail.delay(
            token, user.username, user.email)
        return user


class ResetSerializer(serializers.Serializer):
    """Password reset serializer"""

    password = serializers.CharField(max_length=200,
        validators=[RegexValidator(regex.PASSWORD)])

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserListSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    """User list serializer"""

    class Meta:
        model = User
        exclude = ('password', 'isActive',
            'renewed', 'created', 'modified')
