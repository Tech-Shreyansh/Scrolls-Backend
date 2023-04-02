from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

class Team_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('domain', "topic")
    list_display = ['name',"domain","topic"]

# class Team_admin(admin.ModelAdmin):
#     search_fields = ('domain', "topic")
#     list_display = ['name',"domain","topic"]

admin.site.register(Participant)
admin.site.register(Team,Team_admin)
admin.site.register(Registration_Check)
admin.site.register(OTP)