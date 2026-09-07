from rest_framework import serializers
from .models import Subject, Module, Topic, CodeExample, Problem
from apps.assignments.models import ProblemAccess, Submission


class CodeExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeExample
        fields = ['id', 'topic', 'label', 'code', 'order']


class ProblemAccessSerializer(serializers.ModelSerializer):
    is_active_now = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    seconds_remaining = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProblemAccess
        fields = [
            'is_unlocked', 'unlocked_at', 'deadline',
            'allow_late_submission', 'is_active_now',
            'is_expired', 'seconds_remaining'
        ]


class ProblemSerializer(serializers.ModelSerializer):
    access_control = ProblemAccessSerializer(read_only=True)
    my_submission = serializers.SerializerMethodField()
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    module_name = serializers.CharField(source='topic.module.name', read_only=True)
    module_level = serializers.CharField(source='topic.module.level', read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id', 'topic', 'topic_title', 'module_name', 'module_level',
            'title', 'description', 'expected_output_hint',
            'starter_code', 'test_criteria', 'expected_keywords',
            'points', 'order', 'access_control', 'my_submission'
        ]

    def get_my_submission(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        sub = Submission.objects.filter(student=request.user, problem=obj).first()
        if not sub:
            return None
        return {
            'id': sub.id,
            'status': sub.status,
            'score': sub.score,
            'staff_feedback': sub.staff_feedback,
            'submitted_at': sub.submitted_at,
            'reviewed_at': sub.reviewed_at,
            'submitted_code': sub.submitted_code,
            'notes': sub.notes,
        }


class ProblemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'id', 'topic', 'title', 'description',
            'expected_output_hint', 'starter_code',
            'test_criteria', 'expected_keywords',
            'points', 'order'
        ]


class TopicSerializer(serializers.ModelSerializer):
    examples = CodeExampleSerializer(many=True, read_only=True)
    problems = ProblemSerializer(many=True, read_only=True)
    module_name = serializers.CharField(source='module.name', read_only=True)
    module_level = serializers.CharField(source='module.level', read_only=True)

    class Meta:
        model = Topic
        fields = [
            'id', 'topic_id', 'title', 'module', 'module_name',
            'module_level', 'explain', 'order', 'examples', 'problems'
        ]


class TopicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'module', 'topic_id', 'title', 'explain', 'order']


class ModuleSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    total_topics = serializers.SerializerMethodField()
    total_problems = serializers.SerializerMethodField()
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Module
        fields = [
            'id', 'subject', 'subject_name', 'name', 'level', 'order', 'topics',
            'total_topics', 'total_problems'
        ]

    def get_total_topics(self, obj):
        return obj.topics.count()

    def get_total_problems(self, obj):
        return Problem.objects.filter(topic__module=obj).count()


class ModuleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'subject', 'name', 'level', 'order']


class SubjectSerializer(serializers.ModelSerializer):
    total_modules = serializers.SerializerMethodField()
    total_topics = serializers.SerializerMethodField()
    total_problems = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'icon', 'banner_image', 'instructor_name', 'level',
            'duration', 'order', 'is_active', 'total_modules',
            'total_topics', 'total_problems', 'created_at'
        ]

    def get_total_modules(self, obj):
        return obj.modules.count()

    def get_total_topics(self, obj):
        return Topic.objects.filter(module__subject=obj).count()

    def get_total_problems(self, obj):
        return Problem.objects.filter(topic__module__subject=obj).count()


class SubjectDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    total_modules = serializers.SerializerMethodField()
    total_topics = serializers.SerializerMethodField()
    total_problems = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'icon', 'banner_image', 'instructor_name', 'level',
            'duration', 'order', 'is_active', 'modules',
            'total_modules', 'total_topics', 'total_problems', 'created_at'
        ]

    def get_total_modules(self, obj):
        return obj.modules.count()

    def get_total_topics(self, obj):
        return Topic.objects.filter(module__subject=obj).count()

    def get_total_problems(self, obj):
        return Problem.objects.filter(topic__module__subject=obj).count()


class SubjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'icon', 'banner_image', 'instructor_name', 'level',
            'duration', 'order', 'is_active'
        ]
