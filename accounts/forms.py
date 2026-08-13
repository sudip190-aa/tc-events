from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=100,
        required=True
    )

    last_name = forms.CharField(
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        required=True
    )

    role = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('organizer', 'Club / Organizer'),
        ]
    )

    class Meta:

        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2',
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:

            user.save()

            user.profile.full_name = (
                f"{user.first_name} {user.last_name}"
            )

            user.profile.role = (
                self.cleaned_data['role']
            )

            user.profile.save()

        return user


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            'full_name',
            'phone',
            'bio',
            'profile_picture',
        ]

        widgets = {

            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your full name'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Phone number'
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    'placeholder': 'Tell us about yourself',
                    'rows': 4
                }
            ),
        }