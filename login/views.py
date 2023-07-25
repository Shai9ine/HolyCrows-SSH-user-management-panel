# login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect them to the dashboard or desired page.
        return redirect('/')  # Replace 'dashboard' with the name of your dashboard view or URL pattern

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)  # Get the 'remember_me' checkbox value

            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active and user.is_superuser:
                # Check if the user is active and is a superuser (admin).
                login(request, user)
                if not remember_me:
                    # If 'remember me' is not checked, set the session to expire when the user closes the browser.
                    request.session.set_expiry(0)
                return redirect('/')  # Redirect to the dashboard or desired page upon successful login
            else:
                # Invalid login credentials, show an error message.
                error_message = "Invalid username or password. Please try again."
        else:
            # Form is not valid, show an error message.
            error_message = "Please fill in both username and password fields."
    else:
        form = LoginForm()
        error_message = None

    return render(request, 'login/login_page.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
