from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken 

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
            return Response({'successfully registered'}, status=status.HTTP_201_CREATED)
        return Response({'enter correct details'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self,request):
        email = request.data.get("email")
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            user = Participant.objects.get(email__iexact=email)
            if user.is_ambassador == True:
                return Response({'User is Already a college ambassador'}, status=status.HTTP_409_CONFLICT)
            user.is_ambassador = True
            user.save()
            return Response({'User is made a college ambassador'}, status=status.HTTP_200_OK)
        return Response({"User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

class team(APIView):
    def post(self,request):
        request.data["password"]= make_password(request.data.get("password"))
        team_size = request.data.get("size")
        if request.data.get("referral_used") is not None:
            if(request.data["referral_used"][3:10]==str(request.data["leader_id"])):
                return Response({"cannot use leader's referral code"}, status=status.HTTP_409_CONFLICT)
            if team_size==3:
                if(request.data["referral_used"][3:10]==str(request.data["member_2"])or request.data["referral_used"][3:10]==str(request.data["member_3"])):
                    return Response({"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
            if team_size==2:
                if(request.data["referral_used"][3:10]==str(request.data["member_2"])):
                    return Response({"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
        leader = Participant.objects.filter(member_id=request.data["leader_id"])
        if not leader.exists():
            return Response({"leader's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        request.data["leader_id"] = leader[0].id
        if team_size == 2:
            member_2 = Participant.objects.filter(member_id=request.data["member_2"])
            if not member_2.exists():
                return Response({"member_2's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_2"] = member_2[0].id
        if team_size == 3:
            member_2 = Participant.objects.filter(member_id=request.data["member_2"])
            if not member_2.exists():
                return Response({"member_2's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_2"] = member_2[0].id
            member_3 = Participant.objects.filter(member_id=request.data["member_3"])
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
                return Response({'successfully registered'}, status=status.HTTP_201_CREATED)

# def getTokens(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }
 
class Login_user(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(password)
        user = Participant.objects.filter(email__iexact = email)
        print(user)
        # if not user.exists():
        #     context = {'msg':'user with this mail does not exist'}
        #     return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if user is not None:
            # token = getTokens(user)
            return Response({'id':user.id,'msg':'Login Success'}, status=status.HTTP_200_OK)

        return Response({'msg':'Enter correct Password'}, status=status.HTTP_400_BAD_REQUEST)