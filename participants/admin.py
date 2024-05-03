from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin

class SynopsisSubmittedFilter(admin.SimpleListFilter):
    title = 'Synopsis Submitted'
    parameter_name = 'has_synopsis'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(synopsis='')
        elif self.value() == 'no':
            return queryset.filter(synopsis='')

class PaperSubmittedFilter(admin.SimpleListFilter):
    title = 'Technical Paper Submitted'
    parameter_name = 'has_paper'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(paper='')
        elif self.value() == 'no':
            return queryset.filter(paper='')

class Team_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('name','domain', "topic", "team_id")
    list_display = ['name', "domain", "topic", "team_id","is_selected" , 'has_submitted_synopsis', 'has_submitted_paper']
    exclude = ('password',)
    list_filter = (SynopsisSubmittedFilter,PaperSubmittedFilter, "is_selected", "domain")

    def has_submitted_synopsis(self, obj):
        return obj.synopsis.name != ""

    def has_submitted_paper(self, obj):
        return obj.paper.name != ""

    has_submitted_synopsis.boolean = True
    has_submitted_paper.boolean = True
    has_submitted_synopsis.short_description = 'Synopsis Submitted'
    has_submitted_paper.short_description = 'Technical Paper Submitted'

class Participant_admin(ExportActionMixin, admin.ModelAdmin):
    search_fields = ('name', 'gender', "course", "year_of_study", "is_ambassador")
    list_display = ['email','name','gender', "course", "year_of_study", "college","member_id"]
    exclude = ('password',)

admin.site.register(Participant,Participant_admin)
admin.site.register(Team,Team_admin)
admin.site.register(Registration_Check)
admin.site.register(OTP)
