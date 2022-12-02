from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from staffsys import models
from django import forms
from django.core.paginator import Paginator, Page


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(
        attrs={"class": "form-control", "id": "floatingInput", "placeholder": "name@example.com"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(
        attrs={"class": "form-control", "id": "floatingPassword", "placeholder": "Password"}))


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        pass
    return render(request, 'login.html', {"form": form})