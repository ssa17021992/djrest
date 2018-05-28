from django.urls import include, re_path as path

from .views import (
    SignUpAvailableAPIView,
    SignUpMailAPIView,
    SignUpCheckAPIView,
    SignUpAPIView,
    SignInAPIView,

    SocialSignInAPIView,

    ProfileAPIView,
    AvatarAPIView,

    ChangeAPIView,

    ResetMailAPIView,
    ResetCheckAPIView,
    ResetAPIView,

    UserAPIView,
)


urlpatterns = [
    path(
        r'^accounts/signup/available$',
        SignUpAvailableAPIView.as_view(),
        name='signup-available'
    ),
    path(
        r'^accounts/signup/mail$',
        SignUpMailAPIView.as_view(),
        name='signup-mail'
    ),
    path(
        r'^accounts/signup/check$',
        SignUpCheckAPIView.as_view(),
        name='signup-check'
    ),
    path(
        r'^accounts/signup$',
        SignUpAPIView.as_view(),
        name='accounts-signup'
    ),
    path(
        r'^accounts/signin$',
        SignInAPIView.as_view(),
        name='accounts-signin'
    ),

    path(
        r'^accounts/social/signin$',
        SocialSignInAPIView.as_view(),
        name='social-signin'
    ),

    path(
        r'^accounts/me/profile$',
        ProfileAPIView.as_view(),
        name='me-profile'
    ),
    path(
        r'^accounts/me/avatar$',
        AvatarAPIView.as_view(),
        name='me-avatar'
    ),

    path(
        r'^accounts/me/passwd/change$',
        ChangeAPIView.as_view(),
        name='passwd-change'
    ),

    path(
        r'^accounts/me/passwd/mail$',
        ResetMailAPIView.as_view(),
        name='passwd-mail'
    ),
    path(
        r'^accounts/me/passwd/check$',
        ResetCheckAPIView.as_view(),
        name='passwd-check'
    ),
    path(
        r'^accounts/me/passwd/reset$',
        ResetAPIView.as_view(),
        name='passwd-reset'
    ),

    path(
      r'^users$',
      UserAPIView.as_view(),
      name='user-list'
    ),
]
