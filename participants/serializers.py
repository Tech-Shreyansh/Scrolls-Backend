from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class participant_serializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id","name", "email", "gender", "college", "course", "branch", "year_of_study","mobile","member_id","referral_code","referral_count"]
        extra_kwargs={
            'password':{'required': True},
            'gender':{'required': True},
            'name':{'required': True},
            'college':{'required': True},
            'course':{'required': True},
            'year_of_study':{'required': True},
            'mobile':{'required': True},
        }

class team_serializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ["id","name", "topic", "password", "domain", "size","team_id", "leader_id", "member_2", "member_3","referral_used","synopsis","paper"]
        extra_kwargs={
            'password':{'required': True},
            'name':{'required': True},
            'size':{'required': True},
            'leader_id':{'required': True},
            'member_2':{'required': True},
        }
        

        