from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from appusers.forms import LoginUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'appusers/login.html'
    extra_context = {'title': 'авторизация'}


