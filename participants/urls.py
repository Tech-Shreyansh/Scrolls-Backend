from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', register.as_view(), name='register'),
]