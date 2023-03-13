from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken 
from .mail import *

class register(APIView):
    def post(self, request, pk):
        email = request.data.get("email")
        request.data["password"]= make_password(request.data.get("password"))
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            return Response({'Email Already Exists'}, status=status.HTTP_409_CONFLICT)
        serializer = participant_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  
            # Participant.objects.create_user(email = request.data.get("email"),name = request.data["name"], password = request.data.get("password"))
            if pk=='1':
                serializer.validated_data["is_ambassador"] = True
            serializer.save()
            return Response({'successfully registered! Check your mail for your scroll id'}, status=status.HTTP_201_CREATED)
        return Response({'enter correct details'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self,request):
        email = request.data.get("email")
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            user = Participant.objects.get(email__iexact=email)
            if user.is_ambassador == True:
                return Response({'User is Already a college ambassador'}, status=status.HTTP_409_CONFLICT)
            Participant.objects.filter(email__iexact=email).update(is_ambassador=True)
            send_referral_id(email,user.referral_code)
            return Response({'User is made a college ambassador! Check your mail for your referral id'}, status=status.HTTP_200_OK)
        return Response({"User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

class team(APIView):
    def post(self,request):
        request.data["password"]= make_password(request.data.get("password"))
        leader_id = request.data["leader_id"]
        member_2 = request.data["member_2"]
        member_3 = request.data["member_3"]
        print(leader_id,member_2,member_3)
        team_size = request.data.get("size")
        if(leader_id==member_2 or leader_id == member_3 or member_2==member_3):
            return Response({"2 teammates can't have same scroll id"}, status=status.HTTP_409_CONFLICT)
        if request.data.get("referral_used") is not None:
            if(request.data["referral_used"][3:10]==str(leader_id)):
                return Response({"cannot use leader's referral code"}, status=status.HTTP_409_CONFLICT)
            if team_size==3:
                if(request.data["referral_used"][3:10]==str(member_2)or request.data["referral_used"][3:10]==str(member_3)):
                    return Response({"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
            if team_size==2:
                if(request.data["referral_used"][3:10]==str(member_2)):
                    return Response({"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
        leader = Participant.objects.filter(member_id=leader_id)
        if not leader.exists():
            return Response({"leader's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        request.data["leader_id"] = leader[0].id
        if team_size == 2:
            member_2 = Participant.objects.filter(member_id=member_2)
            if not member_2.exists():
                return Response({"member_2's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_2"] = member_2[0].id
        if team_size == 3:
            member_2 = Participant.objects.filter(member_id=member_2)
            if not member_2.exists():
                return Response({"member_2's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_2"] = member_2[0].id
            member_3 = Participant.objects.filter(member_id=member_3)
            if not member_3.exists():
                return Response({"member_3's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_3"] = member_3[0].id
            referral = request.data.get("referral_used")
            participant = Participant.objects.filter(referral_code=referral)
            if not participant.exists() and referral != None:
                return Response({"Invalid referral id"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = team_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                if referral != None:
                    Participant.objects.filter(referral_code=referral).update(referral_count= participant[0].referral_count + 1)
                return Response({'successfully registered! Check your mail for your team id '}, status=status.HTTP_201_CREATED)

def getTokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
 
class Login_user(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = Participant.objects.filter(email__iexact = email)
        if not user.exists():
            context = {'msg':'user with this email does not exist'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if user is not None:
            token = getTokens(user)
            return Response({'id':user.id,'tokens': token,'msg':'Login Success'}, status=status.HTTP_200_OK)

        return Response({'msg':'Enter correct Password'}, status=status.HTTP_400_BAD_REQUEST)

class Login_team(APIView):
    def post(self, request):
        team_id = request.data.get('team_id')
        password = request.data.get('password')
        team = Team.objects.filter(team_id = team_id)
        if not team.exists():
            leader = Participant.objects.filter(email__iexact=team_id)
            if leader.exists():
                team = Team.objects.filter(leader_id = leader[0])

        if not team.exists():
            context = {'msg':'team with this email/team_id does not exist'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        result = team[0].check_password(password)
        if result is True:
            token = getTokens(team[0])
            return Response({'id':team[0].id,'msg':'Login Success', "tokens" : token}, status=status.HTTP_200_OK)

        return Response({'msg':'Enter correct Password'}, status=status.HTTP_400_BAD_REQUEST)