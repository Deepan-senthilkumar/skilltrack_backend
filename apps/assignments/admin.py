from django.contrib import admin
from .models import ProblemAccess, Submission


@admin.register(ProblemAccess)
class ProblemAccessAdmin(admin.ModelAdmin):
    list_display = ('problem', 'is_unlocked', 'deadline', 'allow_late_submission', 'batch_name')
    list_filter = ('is_unlocked', 'batch_name')
    search_fields = ('problem__title',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'problem', 'status', 'score', 'is_late', 'submitted_at')
    list_filter = ('status', 'is_late')
    search_fields = ('student__username', 'problem__title')
    readonly_fields = ('submitted_at',)
