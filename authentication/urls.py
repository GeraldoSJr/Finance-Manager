from django.urls import path
from .views import RegistrationView, LoginView, UsernameValidationView,\
    EmailValidationView, LogoutView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('validate/', csrf_exempt(UsernameValidationView.as_view()), name="validate"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
