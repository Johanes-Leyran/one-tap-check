from django.shortcuts import render, redirect
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
                    # redirect to admin
                    pass
                elif role == 'TEACHER':
                    return redirect('teacher_dashboard', pk=user.pk)
                elif role == 'STAFF':
                    pass
                    # redirect to staff
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
