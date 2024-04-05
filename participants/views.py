from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken 
from .otp import *
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone
import pylibmagic
import magic
from django.conf import settings
import requests, urllib
from rest_framework.throttling import UserRateThrottle

class register(APIView):
    throttle_classes = [UserRateThrottle]
    def post(self, request, pk):
        check = Registration_Check.objects.all()
        if check[0].is_open == False:
            return Response({"msg":"Registration will begin soon"}, status=status.HTTP_400_BAD_REQUEST)
        secret_key = settings.RECAPTCHA_PRIVATE_KEY
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
            'secret': secret_key,
            'response': request.data.get('g-recaptcha-response'),
            }
        )
        # print(request.data.get('g-recaptcha-response'))
        # print(r)
        # print(r.json()['success'])
        if r.json()['success']:
            mobile = int(request.data.get("mobile"))
            print(mobile)
            if mobile > 9999999999 or mobile < 1000000000 : 
                return Response({'msg':"Enter a valid 10 digit mobile number"}, status=status.HTTP_409_CONFLICT)
            email = request.data.get("email")
            user = Participant.objects.filter(email__iexact=email)
            if user.exists():
                return Response({'msg':'Email Already Exists'}, status=status.HTTP_409_CONFLICT)
            serializer = participant_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):  
                serializer.validated_data["password"]= make_password(request.data.get("password"))
                if pk=='1':
                    serializer.validated_data["is_ambassador"] = True
                serializer.save()
                return Response({'msg':'successfully registered! Check your mail for your scroll id'}, status=status.HTTP_201_CREATED)
            return Response({'msg':'enter correct details'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'msg':'verify captcha'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self,request):
        email = request.data.get("email")
        user = Participant.objects.filter(email__iexact=email)
        if user.exists():
            user = Participant.objects.get(email__iexact=email)
            if user.is_ambassador == True:
                return Response({'msg':'User is Already a college ambassador'}, status=status.HTTP_409_CONFLICT)
            Participant.objects.filter(email__iexact=email).update(is_ambassador=True)
            send_referral_id(email,user.referral_code)
            return Response({'msg':'User is made a college ambassador! Check your mail for your referral id'}, status=status.HTTP_200_OK)
        return Response({'msg':"User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

class team(APIView):
    def post(self,request):
        check = Registration_Check.objects.all()
        if check[0].is_open == False:
            return Response({"msg":"Registration will begin soon"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = team_serializer(data=request.data)
        request.data["password"]= make_password(request.data.get("password"))
        leader_id = request.data["leader_id"]
        member_2 = request.data.get("member_2")
        member_3 = request.data.get("member_3")
        team_size = request.data.get("size")
        if team_size is None or team_size == 1 :
            return Response({'msg':"Team size must be atleast 2"}, status=status.HTTP_409_CONFLICT)
        if team_size==2 and leader_id==member_2:
            return Response({'msg':"2 teammates can't have same scroll id"}, status=status.HTTP_409_CONFLICT)
        if team_size>2:
            if(leader_id==member_2 or leader_id == member_3 or member_2==member_3):
                return Response({'msg':"2 teammates can't have same scroll id"}, status=status.HTTP_409_CONFLICT)
        if request.data.get("referral_used") is not None:
            print(request.data["referral_used"][3:12],str(leader_id))
            if(request.data["referral_used"][3:12]==str(leader_id)):
                return Response({'msg':"cannot use leader's referral code"}, status=status.HTTP_409_CONFLICT)
            if team_size==3:
                if(request.data["referral_used"][3:12]==str(member_2)or request.data["referral_used"][3:12]==str(member_3)):
                    return Response({'msg':"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
            if team_size==2:
                if(request.data["referral_used"][3:12]==str(member_2)):
                    return Response({'msg':"cannot use teammate's referral code"}, status=status.HTTP_409_CONFLICT)
        leader = Participant.objects.filter(member_id=leader_id)
        if not leader.exists():
            return Response({'msg':"leader's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        request.data["leader_id"] = leader[0].id
        if team_size > 1:
            member_2 = Participant.objects.filter(member_id=member_2)
            if not member_2.exists():
                return Response({'msg':"member_2's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_2"] = member_2[0].id
        if team_size > 2:
            member_3 = Participant.objects.filter(member_id=member_3)
            if not member_3.exists():
                return Response({'msg':"member_3's Id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["member_3"] = member_3[0].id
        referral = request.data.get("referral_used")
        participant = Participant.objects.filter(referral_code=referral)
        if not participant.exists() and referral is not None:
            return Response({'msg':"Invalid referral id"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = team_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if referral != None:
                Participant.objects.filter(referral_code=referral).update(referral_count= participant[0].referral_count + 1)
            return Response({'msg':'successfully registered! Check your mail for your team id '}, status=status.HTTP_201_CREATED)
        # return Response({'msg':"Enter Correct details"}, status=status.HTTP_400_BAD_REQUEST)

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

        if user[0].is_ambassador == True:
            result = user[0].check_password(password)
            if result is True:
                return Response({'id':user[0].id,'msg':'Login Success'}, status=status.HTTP_200_OK)
            return Response({'msg':'Enter correct Password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'This user is not a college ambassador'}, status=status.HTTP_400_BAD_REQUEST)

class Login_team(APIView):
    def post(self, request):
        team_id = request.data.get('team_id')
        password = request.data.get('password')
        team = Team.objects.filter(team_id = team_id)
        if not team.exists():
            leader = Participant.objects.filter(email__iexact=team_id)
            if not leader.exists():
                context = {'msg':'this email / team id does not exist'}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            team = Team.objects.filter(leader_id = leader[0])
            if not team.exists():
                return Response({'msg':'team with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        name= team[0].name
        result = team[0].check_password(password)
        user = authenticate(username=name,password=password)
        if result is True:
            token = getTokens(user)
            return Response({'id':team[0].id,'msg':'Login Success', "tokens" : token}, status=status.HTTP_200_OK)

        return Response({'msg':'Invalid Credentials.'}, status=status.HTTP_400_BAD_REQUEST)

def get_member_details(member_id):
    if member_id is not None :
        member_details = Participant.objects.get(id = member_id)
        return participant_serializer(member_details).data

class Team_dashboard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user= request.user
        team = team_serializer(user)
        context = team.data
        context['is_selected'] = Team.objects.get(id=user.id).is_selected
        context['leader_data'] = get_member_details(team.data["leader_id"])
        context['member_2_data'] = get_member_details(team.data["member_2"])
        context['member_3_data'] = get_member_details(team.data["member_3"])
        return Response(context, status=status.HTTP_200_OK)

    def patch(self,request):
        team= request.user
        synopsis = request.data.get("synopsis")
        paper = request.data.get("paper")
        if team.domain != "" and request.data.get("domain") is not None:
            return Response({'msg':'domain is already selected'}, status=status.HTTP_400_BAD_REQUEST)
        if team.topic != "" and request.data.get("topic") is not None:
            return Response({'msg':'topic is already selected'}, status=status.HTTP_400_BAD_REQUEST)
        if synopsis is not None:
            if team.domain == "" and request.data.get("domain") is None:
                return Response({'msg':'Select your domain before synopsis submission'}, status=status.HTTP_400_BAD_REQUEST)
            if team.topic == "" and request.data.get("topic") is None:
                return Response({'msg':'Select your topic before synopsis submission'}, status=status.HTTP_400_BAD_REQUEST)
            if team.synopsis == "":
                synopsis_filetype = magic.from_buffer(synopsis.read())
                if not ("PDF" in synopsis_filetype or "Word" in synopsis_filetype):
                    return Response({'msg':'Synopsis must be PDF or Word Document'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if "PDF" in synopsis_filetype:
                        synopsis.name = team.name + ".pdf"
                    else:
                        synopsis.name = team.name + ".doc"
            else:
                return Response({'msg':'Synopsis is already submitted'}, status=status.HTTP_400_BAD_REQUEST)
        if paper is not None:
            if team.paper == "":
                if team.is_selected == False:
                    return Response({'msg':'Paper can only be submitted after selection in Synopsis round'}, status=status.HTTP_400_BAD_REQUEST)
                paper_filetype = magic.from_buffer(paper.read())
                if not ("PDF" in paper_filetype or "Word" in paper_filetype):
                    return Response({'msg':'Paper must be PDF or Word Document'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if "PDF" in paper_filetype:
                        paper.name = team.name + ".pdf"
                    else:
                        paper.name = team.name + ".doc"
            else:
                return Response({'msg':'Paper is already submitted'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = team_serializer(team, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Data Updated'}, status=status.HTTP_200_OK)

class Ca_dashboard(APIView):
    def get(self,request,pk):
        CA = Participant.objects.get(id=pk)
        referral = CA.referral_code
        teams = Team.objects.filter(referral_used=referral)
        list_of_teams = []
        for i in range(len(teams)):
            team_object = {
                'team_name' : teams[i].name,
                'leader' : teams[i].leader_id.name
            }
            list_of_teams.append(team_object)
        CA.member_id = None
        CA_serializer = participant_serializer(CA)
        context = CA_serializer.data
        context['list_of_teams'] = list_of_teams
        leaderboard = Participant.objects.filter(is_ambassador=True).order_by('-referral_count')
        leaderboard_data = []
        for i in range(len(leaderboard)):
            leaderboard_object = {
                'CA_name' : leaderboard[i].name,
                'referral_count' : leaderboard[i].referral_count
            }
            leaderboard_data.append(leaderboard_object)
        context['leaderboard'] = leaderboard_data
        return Response(context, status=status.HTTP_200_OK)

class Forgot_password(APIView):
    def post(self,request,pk):
        secret_key = settings.RECAPTCHA_PRIVATE_KEY
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
            'secret': secret_key,
            'response': request.data['g-recaptcha-response'],
            }
        )
        if r.json()['success']:
            email = request.data.get("email")
            participant = Participant.objects.filter(email__iexact=email)
            if not participant.exists():
                    return Response({'msg':'Enter Valid Email'}, status=status.HTTP_400_BAD_REQUEST)
            if pk==1:
                team = Team.objects.filter(leader_id=participant[0])
                if not team.exists():
                    return Response({'msg':'No Team with This Leader Email id exists'}, status=status.HTTP_400_BAD_REQUEST)
                team_otp = OTP.objects.filter(email=participant[0],is_team=True)
                if team_otp.exists():
                    if team_otp[0].time_created + timedelta(minutes=1) > timezone.now():
                        return Response({'msg':'resend OTP after one minute'},status=status.HTTP_400_BAD_REQUEST) 
                send_otp(email,1)
                return Response({'msg':'check your mail for otp'}, status=status.HTTP_201_CREATED)
            if pk==0:
                member_otp = OTP.objects.filter(email=participant[0],is_member=True)
                if member_otp.exists():
                    if member_otp[0].time_created + timedelta(minutes=1) > timezone.now():
                        return Response({'msg':'resend OTP after one minute'},status=status.HTTP_400_BAD_REQUEST) 
                send_otp(email,0)
                return Response({'msg':'check your mail for otp'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'verify captcha'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self,request,pk):
        email = request.data.get("email")
        otp = request.data.get("otp")
        password =  make_password(request.data.get("password"))
        if pk==1:
            team_otp = OTP.objects.filter(email=email,otp=otp,is_team=True)
            if team_otp.exists():
                team = Team.objects.filter(leader_id=Participant.objects.get(email__iexact=email))
                team.update(password=password)
                team_otp[0].delete()
                return Response({'msg':'Password Updated'}, status=status.HTTP_200_OK)
            return Response({'msg':'generate a new otp request'}, status=status.HTTP_400_BAD_REQUEST)
        member_otp = OTP.objects.filter(email=email,otp=otp,is_member=True)
        if member_otp.exists():
            participant = Participant.objects.filter(email__iexact=email)
            participant.update(password=password)
            member_otp[0].delete()
            return Response({'msg':'Password Updated'}, status=status.HTTP_200_OK)
        return Response({'msg':'generate a new otp request'}, status=status.HTTP_400_BAD_REQUEST)

class Check_OTP(APIView):
    def post(self,request,pk):
        email = request.data.get("email")
        otp = request.data.get("otp")
        if not len(str(otp)) == 4:
            return Response({'msg':'generate new otp request'}, status=status.HTTP_400_BAD_REQUEST)

        if pk == 1:
            team = OTP.objects.filter(email=email,otp=otp,is_team=True)
            if team.exists():
                if team[0].time_created + timedelta(minutes=2) < timezone.now():
                    return Response({'msg':'OTP expired'},status=status.HTTP_400_BAD_REQUEST) 
                return Response({'msg':'Verification Successful! Reset your password'}, status=status.HTTP_200_OK)
            return Response({"msg":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            member = OTP.objects.filter(email=email,otp=otp,is_member=True)
            if member.exists():
                if member[0].time_created + timedelta(minutes=2) < timezone.now():
                    return Response({'msg':'OTP expired'},status=status.HTTP_400_BAD_REQUEST) 
                return Response({'msg':'Verification Successful! Reset your password'}, status=status.HTTP_200_OK)
            return Response({"msg":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class Check_registration(APIView):
    def get(self,request):
        check = Registration_Check.objects.all()
        if check[0].is_open == True:
            return Response({"msg":"Registration Is Open"}, status=status.HTTP_200_OK)
        return Response({"msg":"Registration will begin soon"}, status=status.HTTP_400_BAD_REQUEST)
