from django.urls import path

from . import views


urlpatterns = [

    path(
        'register/<slug:slug>/',
        views.register_event,
        name='register_event'
    ),

    path(
        'cancel/<uuid:ticket_id>/',
        views.cancel_registration,
        name='cancel_registration'
    ),

    path(
        'my-events/',
        views.my_registrations,
        name='my_registrations'
    ),

    path(
        'ticket/<uuid:ticket_id>/',
        views.ticket_detail,
        name='ticket_detail'
    ),

    path(
        'ticket/<uuid:ticket_id>/qr/',
        views.ticket_qr,
        name='ticket_qr'
    ),

]