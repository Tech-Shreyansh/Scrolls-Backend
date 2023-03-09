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

def check_id(participant,participant_type):
    participant = Participant.objects.filter(member_id=participant)
    if not participant.exists():
        return Response({'msg': participant_type +"'s Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
    return participant[0]
    
class team(APIView):
    def post(self,request):
        request.data["password"]= make_password(request.data.get("password"))
        team_size = request.data.get("size")
        print(request.data["referral_used"][3:10])
        print(request.data["leader_id"])
        if(request.data["referral_used"][3:10]==str(request.data["leader_id"])):
            return Response({'msg':"cannot use leader's referral code"}, status=status.HTTP_409_CONFLICT)
        if team_size==3:
            if(request.data["referral_used"][3:10]==str(request.data["member_2"])or request.data["referral_used"][3:10]==str(request.data["member_3"])):
                return Response({'msg':"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
        if team_size==2:
            if(request.data["referral_used"][3:10]==str(request.data["member_2"])):
                return Response({'msg':"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
        leader = check_id(request.data.get("leader_id"),"leader")
        request.data["leader_id"] = leader.id
        if team_size == 2:
            member_2 = check_id(request.data.get("member_2"),"member_2")
            request.data["member_2"]= member_2.id
        if team_size == 3:
            member_2 = check_id(request.data.get("member_2"),"member_2")
            request.data["member_2"]= member_2.id
            member_3 = check_id(request.data.get("member_3"),"member_3")
            request.data["member_3"]= member_3.id
        referral = request.data.get("referral_used")
        participant = Participant.objects.filter(referral_code=referral)
        if not participant.exists() and referral != None:
            return Response({'msg':"Invalid referral id"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = team_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if referral != None:
                Participant.objects.filter(referral_code=referral).update(referral_count= participant[0].referral_count + 1)
            return Response({'msg':'successfully registered'}, status=status.HTTP_201_CREATED)


        
        

