from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from events.models import Event


def home(request):

    today = timezone.localdate()

    upcoming_events = (
        Event.objects
        .filter(
            status='published',
            event_date__gte=today
        )
        .select_related(
            'category',
            'organizer'
        )
        .order_by(
            'event_date',
            'start_time'
        )[:6]
    )

    latest_events = (
        Event.objects
        .filter(
            status='published'
        )
        .select_related(
            'category',
            'organizer'
        )
        .order_by(
            '-created_at'
        )[:3]
    )

    categories = (
        Event.objects
        .filter(
            status='published'
        )
        .values(
            'category__id',
            'category__name'
        )
        .annotate(
            event_count=Count('id')
        )
        .order_by(
            '-event_count'
        )[:6]
    )

    total_events = Event.objects.filter(
        status='published'
    ).count()

    return render(
        request,
        'core/home.html',
        {
            'upcoming_events': upcoming_events,
            'latest_events': latest_events,
            'categories': categories,
            'total_events': total_events,
        }
    )


def about(request):

    return render(
        request,
        'events/about.html'
    )


def contact(request):

    return render(
        request,
        'core/contact.html'
    )