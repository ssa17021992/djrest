from django.utils.translation import gettext_lazy as _


# Accounts
USER_DOES_NOT_EXIST = {
  'code': 'USER_DOES_NOT_EXIST',
  'detail': _('User does not exist.')
}

INCORRECT_PASSWORD = {
  'code': 'INCORRECT_PASSWORD',
  'detail': _('Incorrect password.')
}

USER_INACTIVE = {
  'code': 'USER_INACTIVE',
  'detail': _('User inactive.')
}

USERNAME_ALREADY_IN_USE = {
  'code': 'USERNAME_ALREADY_IN_USE',
  'detail': _('Username already in use.')
}

INVALID_SIGN_UP_CODE = {
  'code': 'INVALID_SIGN_UP_CODE',
  'detail': _('Invalid sign up code.')
}

SOCIAL_DOES_NOT_EXIST = {
  'code': 'SOCIAL_DOES_NOT_EXIST',
  'detail': _('Social does not exist.')
}

INVALID_TOKEN = {
  'code': 'INVALID_TOKEN',
  'detail': _('Invalid token.')
}

SAME_PASSWORD = {
  'code': 'SAME_PASSWORD',
  'detail': _('Current and new password cannot be same.')
}

FACEBOOK_API_CONNECTION_ERROR = {
  'code': 'FACEBOOK_API_CONNECTION_ERROR',
  'detail': _('Facebook api connection error.')
}

# Common
FORM_ERROR = {
  'code': 'FORM_ERROR',
  'detail': ''
}
