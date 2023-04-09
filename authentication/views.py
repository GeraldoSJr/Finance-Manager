from django.shortcuts import render
from django.views import View


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')


class NewPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/set-newpassword.html')
