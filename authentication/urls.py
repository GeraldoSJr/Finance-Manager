from django.urls import path
from .views import RegistrationView, LoginView, NewPasswordView, ResetPasswordView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
    path('newpassword/', NewPasswordView.as_view(), name="newpassword"),
]
