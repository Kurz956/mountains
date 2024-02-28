from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from Mountains import settings
from appusers.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'appusers/login.html'
    extra_context = {'title': 'авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'appusers/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'appusers/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'default_image': settings.DEFAULT_USER_IMAGE
    }


    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'appusers/password_change_form.html'
    extra_context = {'title': 'Изменения пароля'}
    success_url = reverse_lazy('users:password_change_done')
