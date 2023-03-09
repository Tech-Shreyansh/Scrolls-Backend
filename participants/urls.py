from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/<str:pk>', register.as_view(), name='register'),
    path('register', register.as_view(), name='register'),
]