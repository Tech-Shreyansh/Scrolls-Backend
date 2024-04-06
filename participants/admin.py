from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

class Team_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('domain', "topic","team_id")
    list_display = ['name',"domain","topic","team_id"]
    exclude = ('password',)

class Participant_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('gender', "course", "year_of_study", "is_ambassador")
    list_display = ['email','name','gender', "course", "year_of_study", "college","member_id"]
    exclude = ('password',)

admin.site.register(Participant,Participant_admin)
admin.site.register(Team,Team_admin)
admin.site.register(Registration_Check)
admin.site.register(OTP)