from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class participant_serializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id","name", "email", "password", "gender", "college", "course", "branch", "year_of_study","mobile"]
        extra_kwargs={
            'password':{'write_only': True},
        }