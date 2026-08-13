from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'attendee',
        'event',
        'ticket_id',
        'status',
        'registered_at',
        'attended_at',
    )

    list_filter = (
        'status',
        'registered_at',
        'event',
    )

    search_fields = (
        'attendee__username',
        'attendee__email',
        'event__title',
        'ticket_id',
    )

    readonly_fields = (
        'ticket_id',
        'registered_at',
        'attended_at',
    )