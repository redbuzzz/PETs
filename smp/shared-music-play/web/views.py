from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from web.forms import AuthForm
from web.models import User


def registration_view(request):
    form = AuthForm()
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            user = authenticate(request, **form.cleaned_data)
            login(request, user)
            return redirect("homepage")
    return render(request, "web/registration.html", {"form": form})


def login_view(request):
    form = AuthForm()
    message = None
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = "Неверно указана почта или пароль"
            else:
                login(request, user)
                return redirect("homepage")
    return render(request, "web/login.html", {"form": form, "message": message})


def logout_view(request):
    logout(request)
    return redirect("login")


def homepage_view(request):
    return render(request, "web/homepage.html")
