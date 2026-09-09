from django.contrib import admin
from .models import (
    Subject, Module, Topic, CodeExample, Problem, TopicImage,
    Batch, BatchTopicProgress, StaffDailyLog, StudentAttendanceRecord,
    PlatformCapability
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'duration', 'schedule_type', 'level', 'is_active', 'order']
    list_filter = ('is_active', 'level')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    show_full_result_count = False


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'schedule', 'status', 'start_date', 'student_count']
    list_select_related = ('course',)
    list_filter = ('status', 'course')
    search_fields = ('name', 'course__name', 'schedule')
    filter_horizontal = ('staff', 'students')
    show_full_result_count = False


@admin.register(BatchTopicProgress)
class BatchTopicProgressAdmin(admin.ModelAdmin):
    list_display = ['batch', 'topic', 'is_completed', 'completed_at', 'marked_by']
    list_select_related = ('batch', 'topic', 'marked_by')
    list_filter = ('is_completed', 'batch')
    search_fields = ('batch__name', 'topic__title')
    show_full_result_count = False


@admin.register(StaffDailyLog)
class StaffDailyLogAdmin(admin.ModelAdmin):
    list_display = ['date', 'batch', 'course', 'staff', 'session_type', 'students_attended', 'total_enrolled']
    list_select_related = ('batch', 'course', 'staff')
    list_filter = ('date', 'session_type', 'course', 'staff')
    search_fields = ('batch__name', 'course__name', 'staff__username', 'remarks')
    show_full_result_count = False


@admin.register(StudentAttendanceRecord)
class StudentAttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['daily_log', 'student', 'is_present']
    list_select_related = ('daily_log', 'student')
    list_filter = ('is_present',)
    search_fields = ('student__username', 'daily_log__batch__name')
    show_full_result_count = False


class TopicImageInline(admin.TabularInline):
    model = TopicImage
    extra = 0
    fields = ('image_url', 'caption', 'order')


class CodeExampleInline(admin.StackedInline):
    model = CodeExample
    extra = 0


class ProblemInline(admin.StackedInline):
    model = Problem
    extra = 0


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'level', 'order']
    list_select_related = ('subject',)
    list_filter = ('level', 'subject')
    search_fields = ('name',)
    show_full_result_count = False
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic_id', 'module', 'order']
    list_select_related = ('module', 'module__subject')
    list_filter = ('module__level', 'module__subject')
    search_fields = ('title', 'topic_id')
    raw_id_fields = ('module',)
    show_full_result_count = False
    inlines = [TopicImageInline, CodeExampleInline, ProblemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('module__subject')


@admin.register(TopicImage)
class TopicImageAdmin(admin.ModelAdmin):
    list_display = ['topic', 'caption', 'order', 'uploaded_at']
    list_select_related = ('topic',)
    search_fields = ('topic__title', 'caption')
    raw_id_fields = ('topic',)
    show_full_result_count = False


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'language', 'points', 'order']
    list_select_related = ('topic', 'topic__module')
    list_filter = ('language',)
    search_fields = ('title', 'description', 'expected_output')
    raw_id_fields = ('topic',)
    show_full_result_count = False


@admin.register(PlatformCapability)
class PlatformCapabilityAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'icon', 'order', 'is_active']
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    show_full_result_count = False
