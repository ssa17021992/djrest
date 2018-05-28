from django.contrib import admin

from .models import User, SocialLogin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin"""

    exclude = ('renewed',)
    list_display = ('username', 'email',
        'isActive', 'created', 'modified')
    list_filter = ('isActive',)

    search_fields = ('firstName',
        'middleName', 'lastName', 'username', 'email')


@admin.register(SocialLogin)
class SocialLoginAdmin(admin.ModelAdmin):
    """Social login admin"""

    list_display = ('user', 'social', 'created')

    search_fields = ('social', 'user__username')
