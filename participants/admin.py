from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

class Team_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('domain', "topic")
    list_display = ['name',"domain","topic"]
    exclude = ('password',)

class Participant_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('gender', "course", "year_of_study", "is_ambassador")
    list_display = ['email','name','gender', "course", "year_of_study", "college"]
    exclude = ('password',)

admin.site.register(Participant,Participant_admin)
admin.site.register(Team,Team_admin)
admin.site.register(Registration_Check)
admin.site.register(OTP)