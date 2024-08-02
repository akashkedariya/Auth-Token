from django.urls import path
from . import views
# from Auth.views import UserRegistrationView #UserLoginView, UserProfileView, UserRegistrationView,Demo,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register/',views.RegisteruserView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change_password/',views.UserChangePasswordView.as_view(),name="change_password"),
    path('send_reset_password_email/', views.SendPasswordResetEmailView.as_view()),                     # Email not working
    path('reset_password/<uid>/<token>/', views.UserPasswordResetView.as_view(),name="reset_password"), # Not Working
]