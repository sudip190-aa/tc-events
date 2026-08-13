from django import forms

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            'title',
            'description',
            'category',
            'image',
            'venue',
            'address',
            'event_date',
            'start_time',
            'end_time',
            'registration_deadline',
            'capacity',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder':
                    'e.g. Texas College Tech Summit'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder':
                    'Describe your event...',
                    'rows': 7
                }
            ),

            'event_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),

            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                }
            ),

            'registration_deadline': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),

            'capacity': forms.NumberInput(
                attrs={
                    'min': 1,
                    'placeholder': '100'
                }
            ),

            'venue': forms.TextInput(
                attrs={
                    'placeholder':
                    'e.g. Main Hall'
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'placeholder':
                    'e.g. Texas College, Kathmandu'
                }
            ),
        }