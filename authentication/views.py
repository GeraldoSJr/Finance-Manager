from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        messages.success(request, "Registration Successfully")
        messages.warning(request, "Registration Warning")
        messages.error(request, "Registration Error")
        messages.info(request, "Registration Info")

        return render(request, 'authentication/register.html')


class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = str(data['username'])

        if not username.isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, username already taken'}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email needs to be valid, example@email.com'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, this email already exists'}, status=409)

        return JsonResponse({'email_valid': True})


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')


class NewPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/set-newpassword.html')
