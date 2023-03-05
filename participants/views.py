from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class register(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            return Response({'msg':'Email'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = participant_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):            
            serializer.save()
            return Response({'msg':'success'}, status=status.HTTP_200_OK)
        return Response({'msg':'enter correct details'}, status=status.HTTP_400_BAD_REQUEST)