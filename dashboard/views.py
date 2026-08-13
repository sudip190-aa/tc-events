from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.db.models import Count

from django.utils import timezone

from events.models import Event

from registrations.models import Registration


@login_required
def dashboard_redirect(request):

    user = request.user

    # Django superuser
    if user.is_superuser:
        return redirect('admin_dashboard')

    # Check profile role
    if hasattr(user, 'profile'):

        role = user.profile.role

        if role == 'organizer':
            return redirect('organizer_dashboard')

        if role == 'admin':
            return redirect('admin_dashboard')

    return redirect('student_dashboard')


@login_required
def student_dashboard(request):

    user = request.user

    registrations = Registration.objects.filter(
        attendee=user
    ).select_related(
        'event',
        'event__category'
    )

    active_registrations = registrations.filter(
        status__in=[
            'confirmed',
            'attended'
        ]
    )

    attended_events = registrations.filter(
        status='attended'
    ).count()

    upcoming_events = active_registrations.filter(
        event__event_date__gte=timezone.localdate()
    ).order_by(
        'event__event_date',
        'event__start_time'
    )[:5]

    return render(
        request,
        'dashboard/student_dashboard.html',
        {
            'registrations': registrations,
            'active_registrations': active_registrations,
            'attended_events': attended_events,
            'upcoming_events': upcoming_events,
        }
    )


@login_required
def organizer_dashboard(request):

    user = request.user

    if not hasattr(user, 'profile'):

        messages.error(
            request,
            'Organizer profile not found.'
        )

        return redirect('student_dashboard')

    if user.profile.role != 'organizer':

        messages.error(
            request,
            'You do not have organizer access.'
        )

        return redirect('dashboard')

    events = Event.objects.filter(
        organizer=user
    )

    total_events = events.count()

    published_events = events.filter(
        status='published'
    ).count()

    pending_events = events.filter(
        status='pending'
    ).count()

    total_registrations = Registration.objects.filter(
        event__organizer=user,
        status__in=[
            'confirmed',
            'attended'
        ]
    ).count()

    recent_events = events.order_by(
        '-created_at'
    )[:5]

    recent_registrations = Registration.objects.filter(
        event__organizer=user
    ).select_related(
        'event',
        'attendee'
    ).order_by(
        '-registered_at'
    )[:8]

    return render(
        request,
        'dashboard/organizer_dashboard.html',
        {
            'events': events,
            'total_events': total_events,
            'published_events': published_events,
            'pending_events': pending_events,
            'total_registrations': total_registrations,
            'recent_events': recent_events,
            'recent_registrations': recent_registrations,
        }
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:

        if not hasattr(request.user, 'profile'):

            messages.error(
                request,
                'You do not have administrator access.'
            )

            return redirect('student_dashboard')

        if request.user.profile.role != 'admin':

            messages.error(
                request,
                'You do not have administrator access.'
            )

            return redirect('dashboard')

    total_users = User.objects.count()

    total_events = Event.objects.count()

    published_events = Event.objects.filter(
        status='published'
    ).count()

    pending_events = Event.objects.filter(
        status='pending'
    ).count()

    total_registrations = Registration.objects.count()

    total_attendance = Registration.objects.filter(
        status='attended'
    ).count()

    recent_events = Event.objects.select_related(
        'organizer',
        'category'
    ).order_by(
        '-created_at'
    )[:8]

    pending_event_list = Event.objects.filter(
        status='pending'
    ).select_related(
        'organizer',
        'category'
    ).order_by(
        '-created_at'
    )

    recent_registrations = Registration.objects.select_related(
        'attendee',
        'event'
    ).order_by(
        '-registered_at'
    )[:8]

    return render(
        request,
        'dashboard/admin_dashboard.html',
        {
            'total_users': total_users,
            'total_events': total_events,
            'published_events': published_events,
            'pending_events': pending_events,
            'total_registrations': total_registrations,
            'total_attendance': total_attendance,
            'recent_events': recent_events,
            'pending_event_list': pending_event_list,
            'recent_registrations': recent_registrations,
        }
    )


@login_required
def approve_event(request, event_id):

    if not request.user.is_superuser:

        if (
            not hasattr(request.user, 'profile')
            or request.user.profile.role != 'admin'
        ):

            messages.error(
                request,
                'You do not have permission to approve events.'
            )

            return redirect('dashboard')

    event = get_object_or_404(
        Event,
        id=event_id
    )

    event.status = 'published'

    event.save(
        update_fields=['status']
    )

    messages.success(
        request,
        f'"{event.title}" has been approved.'
    )

    return redirect('admin_dashboard')


@login_required
def reject_event(request, event_id):

    if not request.user.is_superuser:

        if (
            not hasattr(request.user, 'profile')
            or request.user.profile.role != 'admin'
        ):

            messages.error(
                request,
                'You do not have permission to reject events.'
            )

            return redirect('dashboard')

    event = get_object_or_404(
        Event,
        id=event_id
    )

    event.status = 'rejected'

    event.save(
        update_fields=['status']
    )

    messages.warning(
        request,
        f'"{event.title}" has been rejected.'
    )

    return redirect('admin_dashboard')