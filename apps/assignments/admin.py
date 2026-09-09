from django.contrib import admin
from .models import ProblemAccess, Submission


@admin.register(ProblemAccess)
class ProblemAccessAdmin(admin.ModelAdmin):
    list_display = ('problem', 'is_unlocked', 'deadline', 'allow_late_submission', 'batch')
    list_filter = ('is_unlocked', 'batch')
    search_fields = ('problem__title',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'problem', 'batch', 'language', 'is_passed', 'status', 'execution_time_ms', 'attempt_number', 'submitted_at')
    list_filter = ('status', 'is_passed', 'language', 'batch')
    search_fields = ('student__username', 'problem__title', 'batch__name')
    readonly_fields = ('submitted_at',)
