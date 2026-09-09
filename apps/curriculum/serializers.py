from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Subject, Module, Topic, CodeExample, Problem,
    Batch, BatchTopicProgress, StaffDailyLog, StudentAttendanceRecord
)

User = get_user_model()


class ProblemSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    module_id = serializers.IntegerField(source='topic.module.id', read_only=True)
    subject_slug = serializers.CharField(source='topic.module.subject.slug', read_only=True)

    class Meta:
        model = Problem
        fields = [
            'id', 'topic', 'topic_title', 'module_id', 'subject_slug',
            'title', 'description', 'language', 'expected_output',
            'expected_output_hint', 'starter_code', 'test_criteria',
            'expected_keywords', 'points', 'order'
        ]


class CodeExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeExample
        fields = ['id', 'topic', 'label', 'code', 'order']


class TopicSerializer(serializers.ModelSerializer):
    topic_id = serializers.SlugField(required=False, allow_blank=True, validators=[])
    problems = ProblemSerializer(many=True, read_only=True)
    examples = CodeExampleSerializer(many=True, read_only=True)
    module_name = serializers.CharField(source='module.name', read_only=True)
    subject_id = serializers.IntegerField(source='module.subject.id', read_only=True)
    subject_name = serializers.CharField(source='module.subject.name', read_only=True)

    class Meta:
        model = Topic
        fields = [
            'id', 'module', 'module_name', 'subject_id', 'subject_name',
            'topic_id', 'title', 'explain', 'notes_content', 'order',
            'problems', 'examples'
        ]

    def create(self, validated_data):
        from django.utils.text import slugify
        base_slug = validated_data.get('topic_id') or slugify(validated_data.get('title', 'topic')) or 'topic'
        topic_id = base_slug
        counter = 1
        while Topic.objects.filter(topic_id=topic_id).exists():
            topic_id = f"{base_slug}-{counter}"
            counter += 1
        validated_data['topic_id'] = topic_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        from django.utils.text import slugify
        if 'topic_id' in validated_data and validated_data['topic_id']:
            base_slug = validated_data['topic_id']
        else:
            base_slug = instance.topic_id or slugify(validated_data.get('title', instance.title))
        topic_id = base_slug
        counter = 1
        while Topic.objects.filter(topic_id=topic_id).exclude(pk=instance.pk).exists():
            topic_id = f"{base_slug}-{counter}"
            counter += 1
        validated_data['topic_id'] = topic_id
        return super().update(instance, validated_data)


class ModuleSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'subject', 'subject_name', 'name', 'level', 'order', 'topics']


class SubjectSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, allow_blank=True, validators=[])
    modules = ModuleSerializer(many=True, read_only=True)
    batch_count = serializers.SerializerMethodField()
    topic_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'duration', 'schedule_type', 'level', 'icon', 'banner_image',
            'instructor_name', 'order', 'is_active', 'created_at',
            'modules', 'batch_count', 'topic_count'
        ]

    def create(self, validated_data):
        from django.utils.text import slugify
        base_slug = validated_data.get('slug') or slugify(validated_data.get('name', 'subject')) or 'subject'
        slug = base_slug
        counter = 1
        while Subject.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        validated_data['slug'] = slug
        return super().create(validated_data)

    def update(self, instance, validated_data):
        from django.utils.text import slugify
        if 'slug' in validated_data and validated_data['slug']:
            base_slug = validated_data['slug']
        else:
            base_slug = instance.slug or slugify(validated_data.get('name', instance.name))
        slug = base_slug
        counter = 1
        while Subject.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        validated_data['slug'] = slug
        return super().update(instance, validated_data)

    def get_batch_count(self, obj):
        if hasattr(obj, '_prefetched_objects_cache') and 'batches' in obj._prefetched_objects_cache:
            return len(obj.batches.all())
        return obj.batches.count()

    def get_topic_count(self, obj):
        if hasattr(obj, '_prefetched_objects_cache') and 'modules' in obj._prefetched_objects_cache:
            total = 0
            for m in obj.modules.all():
                if hasattr(m, '_prefetched_objects_cache') and 'topics' in m._prefetched_objects_cache:
                    total += len(m.topics.all())
                else:
                    total += m.topics.count()
            return total
        return Topic.objects.filter(module__subject=obj).count()


# Batch Serializers
class BatchUserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_number', 'role']


class BatchTopicProgressSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    topic_order = serializers.IntegerField(source='topic.order', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.display_name', read_only=True)

    class Meta:
        model = BatchTopicProgress
        fields = [
            'id', 'batch', 'topic', 'topic_title', 'topic_order',
            'is_completed', 'completed_at', 'marked_by', 'marked_by_name', 'remarks'
        ]


class BatchSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    staff_details = BatchUserMiniSerializer(source='staff', many=True, read_only=True)
    student_details = BatchUserMiniSerializer(source='students', many=True, read_only=True)
    student_count = serializers.IntegerField(read_only=True)
    progress_stats = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = [
            'id', 'name', 'course', 'course_name', 'course_slug',
            'staff', 'staff_details', 'students', 'student_details',
            'schedule', 'start_date', 'end_date', 'status', 'max_students',
            'student_count', 'created_at', 'progress_stats'
        ]

    def get_progress_stats(self, obj):
        total_topics = Topic.objects.filter(module__subject=obj.course).count()
        completed_topics = obj.topic_progress.filter(is_completed=True).count()
        percent = int((completed_topics / total_topics * 100)) if total_topics > 0 else 0
        return {
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'remaining_topics': max(0, total_topics - completed_topics),
            'progress_percent': percent
        }


# Staff Daily Task / Performance Log Serializers
class StudentAttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.display_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = StudentAttendanceRecord
        fields = ['id', 'daily_log', 'student', 'student_name', 'student_username', 'is_present', 'remarks']


class StaffDailyLogSerializer(serializers.ModelSerializer):
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    staff_name = serializers.CharField(source='staff.display_name', read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    student_attendance = StudentAttendanceRecordSerializer(source='student_attendance_records', many=True, read_only=True)

    class Meta:
        model = StaffDailyLog
        fields = [
            'id', 'date', 'batch', 'batch_name', 'course', 'course_name',
            'staff', 'staff_name', 'session_type', 'session_title', 'topic',
            'topic_title', 'total_enrolled', 'students_attended', 'remarks',
            'created_at', 'updated_at', 'student_attendance'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'batch_name', 'course_name', 'staff_name', 'topic_title']
