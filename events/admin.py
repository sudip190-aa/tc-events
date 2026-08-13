from django.contrib import admin

from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'icon',
        'created_at',
    )

    search_fields = (
        'name',
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'organizer',
        'event_date',
        'venue',
        'status',
        'featured',
    )

    list_filter = (
        'status',
        'category',
        'featured',
        'event_date',
    )

    search_fields = (
        'title',
        'description',
        'venue',
    )

    readonly_fields = (
        'slug',
        'created_at',
        'updated_at',
    )

    list_editable = (
        'status',
        'featured',
    )