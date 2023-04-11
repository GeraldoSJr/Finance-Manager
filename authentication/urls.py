from django.urls import path
from .views import RegistrationView, LoginView, NewPasswordView, ResetPasswordView, UsernameValidationView,\
    EmailValidationView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('validate/', csrf_exempt(UsernameValidationView.as_view()), name="validate"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('login/', LoginView.as_view(), name="login"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
    path('newpassword/', NewPasswordView.as_view(), name="newpassword"),
]
