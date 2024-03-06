from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from recipes.forms import CustomUserCreationForm

def login_view(request):
    error_message = None
    # Remove prefix and initialize form outside of POST check only for rendering purposes
    form = AuthenticationForm()
    registration_form = CustomUserCreationForm(prefix='register')

    if request.method == "POST":
        if 'login' in request.POST:  # Check if the login form was submitted
            # Re-instantiate the form with POST data for login attempts
            form = AuthenticationForm(request, request.POST)
            # Process the login form
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('recipes:list')
                else:
                    error_message = 'Invalid username or password'
        elif 'register' in request.POST:  # Check if the registration form was submitted
            registration_form = CustomUserCreationForm(request.POST, prefix='register')  # Re-instantiate with POST data for registration attempts
            # Process the registration form
            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)  # Log in the user directly after registration
                return redirect('recipes:list')
            else:
                error_message = 'Please correct the errors below'

    context = {
        'form': form,
        'registration_form': registration_form,
        'error_message': error_message
    }
    return render(request, 'auth/login.html', context)

# Ensure the user is logged in before allowing them to access this view.
@login_required
def logout_view(request):
    # Log the user out.
    logout(request)
    # Redirect the user to a success page after logging out.
    return render(request, "auth/success.html")
