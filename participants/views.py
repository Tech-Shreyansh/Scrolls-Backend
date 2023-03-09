from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

class register(APIView):
    def post(self, request, pk):
        email = request.data.get("email")
        request.data["password"]= make_password(request.data.get("password"))
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            return Response({'msg':'Email Already Exists'}, status=status.HTTP_409_CONFLICT)
        serializer = participant_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):   
            if pk=='1':
                serializer.validated_data["is_ambassador"] = True
            serializer.save()
            return Response({'msg':'successfully registered'}, status=status.HTTP_201_CREATED)
        return Response({'msg':'enter correct details'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self,request):
        email = request.data.get("email")
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            user = Participant.objects.get(email__iexact=email)
            if user.is_ambassador == True:
                return Response({'msg':'User is Already a college ambassador'}, status=status.HTTP_409_CONFLICT)
            user.is_ambassador = True
            user.save()
            return Response({'msg':'User is made a college ambassador'}, status=status.HTTP_200_OK)
        return Response({'msg':"User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

