from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LogInForm
from django import forms
from django.contrib.auth import logout, login, authenticate


def login_user(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)

                role = form.cleaned_data['role']
                if role == 'ADMIN':
                    return HttpResponseRedirect(reverse('admin:index'))
                elif role == 'TEACHER':
                    return redirect('teacher_dashboard', pk=user.pk)
                else:
                    form.add_error('role', "Role is invalid")

            else:
                # Invalid login
                form.add_error(None, "Invalid email or password.")
    else:
        form = LogInForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    logout(request)

    return redirect('login')
