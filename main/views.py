from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django_project.settings import STATIC_ROOT
from .forms import UserSignUpForm, UserSignInForm
from .models import MenuItem
from products.models import Product, Category
from django.db.models import Q


def home(request):
    return render(request, 'main/index.html', {'user': request.user, 'url': request.get_full_path})


def sign_up(request):
    form = UserSignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get("password"))
        user = form.save()
        login(request, user)
        return redirect("/")
    return render(request, "main/sign-up.html", {"form": form})


def sign_in(request):
    form = UserSignInForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            request.session["invalid_user"] = True
    return render(request, "main/sign-in.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")
