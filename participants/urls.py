from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/<str:pk>', register.as_view()),
    path('register/', register.as_view()),
    path('team_register/', team.as_view()),
    path('login/', Login_user.as_view()),
    path('team_login/', Login_team.as_view()),
    path('forgot_password/<int:pk>', Send_OTP.as_view()),
    path('verify_otp/<int:pk>', Check_OTP.as_view()),
]
