from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

class Team_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('domain', "topic", "team_id")
    list_display = ['name', "domain", "topic", "team_id", 'has_submitted_synopsis', 'has_submitted_paper']
    exclude = ('password',)

    def has_submitted_synopsis(self, obj):
        return obj.synopsis.name != ""

    def has_submitted_paper(self, obj):
        return obj.paper.name != ""

    has_submitted_synopsis.short_description = 'Synopsis Submitted'
    has_submitted_paper.short_description = 'Technical Paper Submitted'

class Participant_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('gender', "course", "year_of_study", "is_ambassador")
    list_display = ['email','name','gender', "course", "year_of_study", "college","member_id"]
    exclude = ('password',)

admin.site.register(Participant,Participant_admin)
admin.site.register(Team,Team_admin)
admin.site.register(Registration_Check)
admin.site.register(OTP)
