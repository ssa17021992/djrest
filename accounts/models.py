from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import models
from django.core.validators import (
    FileExtensionValidator, RegexValidator,)

from common.models import BaseModel
from common import regex
from common.validators import FileSizeValidator

from .utils import (
    generate_user_renewed,
    generate_code, generate_code_expired,
)


class User(BaseModel):
    """User model"""

    firstName = models.CharField(max_length=150,
        null=False, blank=False, verbose_name=_('first name'))
    middleName = models.CharField(max_length=150,
        null=False, blank=False, verbose_name=_('middle name'))
    lastName = models.CharField(max_length=150,
        null=False, blank=False, verbose_name=_('last name'))

    username = models.CharField(max_length=200,
        unique=True, null=False, blank=False,
        validators=[
            RegexValidator(regex.USERNAME)
        ],
        verbose_name=_('username')
    )

    password = models.CharField(max_length=106,
        null=False, blank=False, verbose_name=_('password'))

    email = models.EmailField(null=False,
        blank=False, verbose_name=_('email address'))
    birthday = models.DateField(null=False,
        blank=False, verbose_name=_('birthday'))
    phone = models.CharField(max_length=15,
        null=False, blank=False, verbose_name=_('phone number'))

    avatar = models.ImageField(null=True, blank=True,
        upload_to='files/avatars/d%Y%m%d/',
        validators=[
            FileExtensionValidator(['png', 'jpg']),
            FileSizeValidator(max_size=1024.0)  # Limited to 1 mb.
        ],
        verbose_name=_('avatar')
    )

    renewed = models.BigIntegerField(default=generate_user_renewed,
        null=True, blank=True, verbose_name=_('renewed'))

    isActive = models.BooleanField(
        default=True, verbose_name=_('active'))

    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(
        auto_now=True, verbose_name=_('modified'))

    @property
    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = make_password(password)
        self.renewed = generate_user_renewed()

    def save(self, *args, **kwargs):
        if not self.password.startswith(
            'pbkdf2_sha256') and len(self.password) != 78:
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('username',)


class SignUpCode(BaseModel):
    """Sign up code model"""

    email = models.EmailField(null=False,
        blank=False, verbose_name=_('email address'))
    code = models.CharField(max_length=4, null=False, blank=False,
        editable=False, default=generate_code, verbose_name=_('code'))

    expired = models.DateTimeField(editable=False,
        default=generate_code_expired, verbose_name=_('expired'))
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created'))

    @property
    def is_valid(self):
        return timezone.now() < self.expired

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'accounts_sign_up_code'
        verbose_name = _('sign up code')
        verbose_name_plural = _('sign up codes')
        ordering = ('email',)


class SocialLogin(BaseModel):
    """Social login model"""

    SOCIALS = (
        ('facebook', _('facebook')),
    )

    social = models.CharField(max_length=10, null=False,
        blank=False, choices=SOCIALS, verbose_name=_('social'))

    user = models.OneToOneField('accounts.User',
        on_delete=models.CASCADE, null=False,
        blank=False, db_column='user', verbose_name=_('user')
    )

    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created'))

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'accounts_social_login'
        verbose_name = _('social login')
        verbose_name_plural = _('social logins')
        ordering = ('created',)
