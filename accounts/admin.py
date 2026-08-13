from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'full_name',
        'role',
        'created_at',
    )

    list_filter = (
        'role',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'full_name',
    )