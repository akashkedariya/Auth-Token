from django.urls import path
from . import views
# from Auth.views import UserRegistrationView #UserLoginView, UserProfileView, UserRegistrationView,Demo,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register/',views.RegisteruserView.as_view()),
    # path('register/',views.UserRegistrationView.as_view()),
]