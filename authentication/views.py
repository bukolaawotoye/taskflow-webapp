from django.shortcuts import render, redirect
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from .models import User
from django.contrib.auth import authenticate, login, logout
from helpers.decorators import auth_user_should_not_access
@auth_user_should_not_access
def register(request):
    """Handles user registration with proper email validation."""
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}

        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        role = request.POST.get('role')

        # Validation checks
        if len(password) < 5:
            messages.error(request, "Password must be at least 5 characters long")
            context['has_error'] = True
        if password != password2:
            messages.error(request, "Passwords do not match")
            context['has_error'] = True
        try:
            validate_email(email, check_deliverability=True)  # Checks domain existence
        except EmailNotValidError:
            messages.error(request, "Invalid email address")
            context["has_error"] = True
        if role not in ['Admin', 'User']:
            messages.error(request, "Invalid role selected")
            messages.error(request, "Role must be either 'Admin' or 'User'")
            context['has_error'] = True
        if not username:
            messages.error(request, "Username is required")
            context['has_error'] = True
        if not role:
            messages.error(request, "Role is required")
            context['has_error'] = True
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            context['has_error'] = True
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            context['has_error'] = True

        # Return with errors if any validations fail
        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        # Create new user (password is properly hashed in create_user)
        user = User.objects.create_user(username=username, email=email, password=password, role=role)

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'authentication/register.html')

@auth_user_should_not_access
def login_view(request):
    """Handles user login using both email and username with extra debugging info."""
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}

        # Get and clean the input data
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        # Debug: log the attempted login identifier
        print("Login attempt for:", username_or_email)

        # Look up the user by email or username (case-insensitive search)
        user_obj = (User.objects.filter(email__iexact=username_or_email).first() or
                    User.objects.filter(username__iexact=username_or_email).first())

        if not user_obj:
            messages.error(request, "Invalid username or password (user not found)")
            context['has_error'] = True
            return render(request, 'authentication/login.html', context)

        # Debug: show the found user's email (which is your unique identifier)
        print("User found:", user_obj.email)

        # Extra check: verify that the provided password matches the stored one directly
        if not user_obj.check_password(password):
            print("Password check failed for user:", user_obj.email)
            messages.error(request, "Invalid username or password (password mismatch)")
            context['has_error'] = True
            return render(request, 'authentication/login.html', context)

        # Since USERNAME_FIELD is "email", call authenticate() with user_obj.email
        user = authenticate(request, username=user_obj.email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            if user.role == "Admin":
                return redirect('home')  # Admins go to home page
            else:
                return redirect('user-tasks')  # Regular users go to their task page
        else:
            # If authentication still fails, log that information
            print("authenticate() returned None for:", user_obj.email)
            messages.error(request, "Invalid username or password (authentication failed)")
            context['has_error'] = True
            return render(request, 'authentication/login.html', context)

    return render(request, 'authentication/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


