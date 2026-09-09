from django.contrib import admin
from .models import (
    Subject, Module, Topic, CodeExample, Problem, TopicImage,
    Batch, BatchTopicProgress, StaffDailyLog, StudentAttendanceRecord
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'duration', 'schedule_type', 'level', 'is_active', 'order')
    list_filter = ('is_active', 'level')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'schedule', 'status', 'start_date', 'student_count')
    list_filter = ('status', 'course')
    search_fields = ('name', 'course__name', 'schedule')
    filter_horizontal = ('staff', 'students')


@admin.register(BatchTopicProgress)
class BatchTopicProgressAdmin(admin.ModelAdmin):
    list_display = ('batch', 'topic', 'is_completed', 'completed_at', 'marked_by')
    list_filter = ('is_completed', 'batch', 'topic__module__subject')
    search_fields = ('batch__name', 'topic__title')


@admin.register(StaffDailyLog)
class StaffDailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'batch', 'course', 'staff', 'session_type', 'students_attended', 'total_enrolled')
    list_filter = ('date', 'session_type', 'course', 'staff')
    search_fields = ('batch__name', 'course__name', 'staff__username', 'remarks')


@admin.register(StudentAttendanceRecord)
class StudentAttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('daily_log', 'student', 'is_present')
    list_filter = ('is_present', 'daily_log__date')
    search_fields = ('student__username', 'daily_log__batch__name')


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
    list_display = ('name', 'subject', 'level', 'order')
    list_filter = ('level', 'subject')
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic_id', 'module', 'order')
    list_filter = ('module__level', 'module', 'module__subject')
    search_fields = ('title', 'topic_id')
    inlines = [TopicImageInline, CodeExampleInline, ProblemInline]


@admin.register(TopicImage)
class TopicImageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'caption', 'order', 'uploaded_at')
    list_filter = ('topic__module__subject',)
    search_fields = ('topic__title', 'caption')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'language', 'points', 'order')
    list_filter = ('language', 'topic__module__subject')
    search_fields = ('title', 'description', 'expected_output')
