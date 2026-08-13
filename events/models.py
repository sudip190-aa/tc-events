from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=20,
        default='🎓'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True
    )

    venue = models.CharField(
        max_length=200
    )

    address = models.CharField(
        max_length=300,
        blank=True
    )

    event_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    registration_deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    capacity = models.PositiveIntegerField(
        default=100
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-event_date', '-start_time']

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.title)

            slug = base_slug

            counter = 1

            while Event.objects.filter(
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):

        return self.title

    @property
    def is_upcoming(self):

        from django.utils import timezone

        return self.event_date >= timezone.localdate()

    @property
    def spots_left(self):

        registered = self.registrations.filter(
            status__in=[
                'confirmed',
                'attended'
            ]
        ).count()

        return max(
            self.capacity - registered,
            0
        )

    @property
    def is_full(self):

        return self.spots_left == 0

