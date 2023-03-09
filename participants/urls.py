from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/<str:pk>', register.as_view()),
    path('register/', register.as_view()),
    path('team_register/', team.as_view()),
]