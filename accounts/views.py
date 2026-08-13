from django.shortcuts import render, redirect

from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import (
    RegistrationForm,
    ProfileUpdateForm
)


def register(request):

    if request.method == 'POST':

        form = RegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Welcome to TC Events!'
            )

            return redirect('dashboard')

    else:

        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


@login_required
def profile(request):

    if request.method == 'POST':

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Your profile has been updated.'
            )

            return redirect('profile')

    else:

        form = ProfileUpdateForm(
            instance=request.user.profile
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'form': form
        }
    )


@login_required
def dashboard(request):

    role = request.user.profile.role

    if role == 'student':

        return render(
            request,
            'accounts/dashboard.html',
            {
                'dashboard_type': 'Student'
            }
        )

    elif role == 'organizer':

        return render(
            request,
            'accounts/dashboard.html',
            {
                'dashboard_type': 'Organizer'
            }
        )

    elif role == 'admin':

        return render(
            request,
            'accounts/dashboard.html',
            {
                'dashboard_type': 'College Admin'
            }
        )

    return redirect('home')


def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')