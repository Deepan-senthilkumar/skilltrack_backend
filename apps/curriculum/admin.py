from django.contrib import admin
from .models import Module, Topic, CodeExample, Problem


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


class CodeExampleInline(admin.StackedInline):
    model = CodeExample
    extra = 1


class ProblemInline(admin.StackedInline):
    model = Problem
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order')
    list_filter = ('level',)
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic_id', 'module', 'order')
    list_filter = ('module__level', 'module')
    search_fields = ('title', 'topic_id')
    inlines = [CodeExampleInline, ProblemInline]


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'points', 'order')
    list_filter = ('topic__module__level', 'topic__module')
    search_fields = ('title', 'description')
