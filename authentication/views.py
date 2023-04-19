from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth
from django.shortcuts import redirect
from userpreferences.models import UserPreference


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get the data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, 'Password too short')
                return render(request, 'authentication/register.html', context)

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            UserPreference.objects.create(user=user, currency='USD')
            messages.success(request, 'Account created successfully!')
            return redirect('expenses')

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

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'Welcome: ' + user.username)
                return redirect('expenses')

            else:
                messages.error(request, 'Your username or password is wrong, try again or create an account')
                return render(request, 'authentication/login.html')
        else:
            messages.error(request, 'Make sure to fill all fields')
            return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You've been logged out")
        return redirect('login')
