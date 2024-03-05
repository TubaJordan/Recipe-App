from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    # Initialize an error message variable to None.
    error_message = None
    # Create an instance of the AuthenticationForm.
    form = AuthenticationForm()

    # Check if the form was submitted via POST.
    if request.method == "POST":
        # Re-bind the form with POST data.
        form = AuthenticationForm(data=request.POST)

        # Validate the form.
        if form.is_valid():
            # Extract username and password from the form.
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Attempt to authenticate the user.
            user = authenticate(username=username, password=password)
            if user is not None:
                # If user is authenticated, log them in and redirect to the recipe list.
                login(request, user)
                return redirect("recipes:list")
            else:
                # Set an error message if authentication fails.
                error_message = "ooops.. somerthing went wrong"

    # Prepare the context with the form and any error message.
    context = {
        "form": form,
        "error_message": error_message
    }

    # Render and return the login page with the context.
    return render(request, "auth/login.html", context)

# Ensure the user is logged in before allowing them to access this view.
@login_required
def logout_view(request):
    # Log the user out.
    logout(request)
    # Redirect the user to a success page after logging out.
    return render(request, "auth/success.html")
