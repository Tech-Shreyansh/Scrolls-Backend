from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/<str:pk>', register.as_view()),
    path('register/', register.as_view()),
    path('team_register/', team.as_view()),
    path('login/', Login_user.as_view()),
    path('team_login/', Login_team.as_view()),
    path('forgot_password/<int:pk>', Forgot_password.as_view()),
    path('verify_otp/<int:pk>', Check_OTP.as_view()),
    path('team_dashboard/', Team_dashboard.as_view()),
    path('ca_dashboard/<int:pk>', Ca_dashboard.as_view()),
    path('check_registration/', Check_registration.as_view()),
]
