from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db import IntegrityError

from django.http import HttpResponse

from django.utils import timezone

from .models import Registration

from events.models import Event

import qrcode

from io import BytesIO


@login_required
def register_event(request, slug):

    if request.method != 'POST':

        return redirect(
            'event_detail',
            slug=slug
        )


    event = get_object_or_404(
        Event,
        slug=slug,
        status='published'
    )


    # Check registration deadline

    if event.registration_deadline:

        if timezone.now() > event.registration_deadline:

            messages.error(
                request,
                'Registration for this event has closed.'
            )

            return redirect(
                'event_detail',
                slug=slug
            )


    # Check event date

    if event.event_date < timezone.localdate():

        messages.error(
            request,
            'This event has already taken place.'
        )

        return redirect(
            'event_detail',
            slug=slug
        )


    # Check capacity

    registered_count = Registration.objects.filter(
        event=event,
        status__in=[
            'confirmed',
            'attended'
        ]
    ).count()


    if registered_count >= event.capacity:

        messages.error(
            request,
            'Sorry, this event is fully booked.'
        )

        return redirect(
            'event_detail',
            slug=slug
        )


    # Check duplicate registration

    existing = Registration.objects.filter(
        event=event,
        attendee=request.user,
        status__in=[
            'confirmed',
            'attended'
        ]
    ).first()


    if existing:

        messages.info(
            request,
            'You are already registered for this event.'
        )

        return redirect(
            'ticket_detail',
            ticket_id=existing.ticket_id
        )


    try:

        registration = Registration.objects.create(
            event=event,
            attendee=request.user
        )

    except IntegrityError:

        messages.error(
            request,
            'You are already registered for this event.'
        )

        return redirect(
            'event_detail',
            slug=slug
        )


    messages.success(
        request,
        'Registration successful! Your ticket is ready.'
    )

    return redirect(
        'ticket_detail',
        ticket_id=registration.ticket_id
    )


@login_required
def cancel_registration(request, ticket_id):

    registration = get_object_or_404(
        Registration,
        ticket_id=ticket_id,
        attendee=request.user
    )


    if registration.status == 'cancelled':

        messages.info(
            request,
            'This registration is already cancelled.'
        )

        return redirect(
            'my_registrations'
        )


    if request.method == 'POST':

        registration.status = 'cancelled'

        registration.save(
            update_fields=['status']
        )

        messages.success(
            request,
            'Your registration has been cancelled.'
        )

        return redirect(
            'my_registrations'
        )


    return render(
        request,
        'registrations/cancel_registration.html',
        {
            'registration': registration
        }
    )


@login_required
def my_registrations(request):

    registrations = Registration.objects.filter(
        attendee=request.user
    ).select_related(
        'event',
        'event__category'
    )

    return render(
        request,
        'registrations/my_registrations.html',
        {
            'registrations': registrations
        }
    )


@login_required
def ticket_detail(request, ticket_id):

    registration = get_object_or_404(
        Registration.objects.select_related(
            'event',
            'event__category',
            'attendee'
        ),
        ticket_id=ticket_id
    )


    if registration.attendee != request.user:

        messages.error(
            request,
            'You cannot access this ticket.'
        )

        return redirect(
            'my_registrations'
        )


    return render(
        request,
        'registrations/ticket.html',
        {
            'registration': registration
        }
    )


@login_required
def ticket_qr(request, ticket_id):

    registration = get_object_or_404(
        Registration,
        ticket_id=ticket_id
    )


    if registration.attendee != request.user:

        return HttpResponse(
            'Unauthorized',
            status=403
        )


    qr_data = (
        f'TC-EVENTS|'
        f'{registration.ticket_id}|'
        f'{registration.event.slug}'
    )


    qr = qrcode.make(qr_data)


    buffer = BytesIO()

    qr.save(
        buffer,
        format='PNG'
    )

    buffer.seek(0)


    return HttpResponse(
        buffer.getvalue(),
        content_type='image/png'
    )