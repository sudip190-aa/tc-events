from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Registration(models.Model):

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    ]

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    attendee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )

    ticket_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed'
    )

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    attended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-registered_at']

        constraints = [
            models.UniqueConstraint(
                fields=['event', 'attendee'],
                name='unique_event_attendee'
            )
        ]

    def __str__(self):
        return (
            f'{self.attendee.username} - '
            f'{self.event.title}'
        )

    @property
    def is_active(self):

        return self.status in [
            'confirmed',
            'attended'
        ]

    def mark_attended(self):

        self.status = 'attended'

        self.attended_at = timezone.now()

        self.save(
            update_fields=[
                'status',
                'attended_at'
            ]
        )