from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.dashboard_redirect,
        name='dashboard'
    ),

    path(
        'student/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'organizer/',
        views.organizer_dashboard,
        name='organizer_dashboard'
    ),

    path(
        'admin-panel/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'approve/<int:event_id>/',
        views.approve_event,
        name='approve_event'
    ),

    path(
        'reject/<int:event_id>/',
        views.reject_event,
        name='reject_event'
    ),

]