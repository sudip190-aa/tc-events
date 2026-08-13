from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Category
from .forms import EventForm


def event_list(request):

    events = Event.objects.filter(
        status='published'
    ).select_related(
        'category',
        'organizer'
    )

    categories = Category.objects.all()

    search = request.GET.get(
        'search',
        ''
    ).strip()

    category = request.GET.get(
        'category',
        ''
    )

    if search:

        events = events.filter(

            Q(title__icontains=search) |

            Q(description__icontains=search) |

            Q(venue__icontains=search)

        )

    if category:

        events = events.filter(
            category__id=category
        )

    context = {

        'events': events,

        'categories': categories,

        'search': search,

        'selected_category': category,

    }

    return render(
        request,
        'events/event_list.html',
        context
    )


def event_detail(request, slug):

    event = get_object_or_404(
        Event.objects.select_related(
            'category',
            'organizer'
        ),
        slug=slug,
        status='published'
    )

    return render(
        request,
        'events/event_details.html',
        {
            'event': event
        }
    )


@login_required
def create_event(request):

    if request.user.profile.role not in [
        'organizer',
        'admin'
    ]:

        messages.error(
            request,
            'Only organizers can create events.'
        )

        return redirect('event_list')


    if request.method == 'POST':

        form = EventForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            event = form.save(
                commit=False
            )

            event.organizer = request.user

            event.status = 'pending'

            event.save()

            messages.success(
                request,
                'Your event has been submitted for approval.'
            )

            return redirect(
                'my_events'
            )

    else:

        form = EventForm()


    return render(
        request,
        'events/create_event.html',
        {
            'form': form
        }
    )


@login_required
def my_events(request):

    events = Event.objects.filter(
        organizer=request.user
    )

    return render(
        request,
        'events/my_events.html',
        {
            'events': events
        }
    )


@login_required
def edit_event(request, slug):

    event = get_object_or_404(
        Event,
        slug=slug
    )

    if event.organizer != request.user:

        messages.error(
            request,
            'You cannot edit this event.'
        )

        return redirect(
            'my_events'
        )


    if request.method == 'POST':

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event
        )

        if form.is_valid():

            event = form.save(
                commit=False
            )

            event.status = 'pending'

            event.save()

            messages.success(
                request,
                'Event updated and submitted for approval.'
            )

            return redirect(
                'my_events'
            )

    else:

        form = EventForm(
            instance=event
        )


    return render(
        request,
        'events/create_event.html',
        {
            'form': form,
            'editing': True,
            'event': event
        }
    )


@login_required
def delete_event(request, slug):

    event = get_object_or_404(
        Event,
        slug=slug
    )

    if event.organizer != request.user:

        messages.error(
            request,
            'You cannot delete this event.'
        )

        return redirect(
            'my_events'
        )


    if request.method == 'POST':

        event.delete()

        messages.success(
            request,
            'Event deleted successfully.'
        )

        return redirect(
            'my_events'
        )


    return render(
        request,
        'events/delete_event.html',
        {
            'event': event
        }
    )