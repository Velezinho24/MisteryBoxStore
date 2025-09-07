from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm


# Vista para el registro de usuarios
def RegisterView(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(
            request,
            'accounts/register.html',
            {'form': form}
        )

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                'Tu cuenta fue creada correctamente'
            )
            return redirect('home')
        return render(
            request,
            'accounts/register.html',
            {'form': form}
        )


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(
        request,
        "accounts/login.html"
    )


def LogoutView(request):
    logout(request)
    return redirect("login")