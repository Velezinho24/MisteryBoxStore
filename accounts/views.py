from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


def register_view(request):
    """
    Register a new user with UserRegistrationForm.
    """
    if request.method == "GET":
        form = UserRegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    # POST
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, _("Your account has been created."))
        # Usa el namespace del home: "home:home"
        return redirect("home:home")

    # Errores de validación
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """
    Authenticate an existing user with username/password fields.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _("Welcome back!"))
            return redirect("home:home")
        messages.error(request, _("Invalid username or password"))

    # GET o POST con error
    return render(request, "accounts/login.html")


def logout_view(request):
    """
    Log out current user and redirect to login page.
    """
    logout(request)
    messages.info(request, _("You have been logged out."))
    # Redirige usando el namespace de accounts
    return redirect("accounts:login")


@login_required
def profile_view(request):
    """
    Vista del perfil del usuario con opción para editar.
    """
    # Asegurar que el usuario tiene perfil
    if not hasattr(request.user, 'profile'):
        from .models import UserProfile
        UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Your profile has been updated successfully!"))
            return redirect('accounts:profile')
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile.html', context)
