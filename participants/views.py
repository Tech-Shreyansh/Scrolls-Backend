from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

class register(APIView):
    def post(self, request):
        email = request.data.get("email")
        request.data["password"]= make_password(request.data.get("password"))
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            return Response({'msg':'Email Already Exists'}, status=status.HTTP_409_CONFLICT)
        serializer = participant_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):            
            serializer.save()
            return Response({'msg':'successfully registered'}, status=status.HTTP_201_CREATED)
        return Response({'msg':'enter correct details'}, status=status.HTTP_406_NOT_ACCEPTABLE)

