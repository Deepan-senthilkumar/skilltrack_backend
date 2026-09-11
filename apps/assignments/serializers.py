from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.curriculum.models import Problem, Batch
from .models import ProblemAccess, Submission

User = get_user_model()


class ProblemAccessControlSerializer(serializers.ModelSerializer):
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    is_active_now = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProblemAccess
        fields = ['id', 'problem', 'problem_title', 'is_unlocked', 'unlocked_at', 'deadline', 'allow_late_submission', 'is_active_now']


class ProblemAccessUpdateSerializer(serializers.Serializer):
    is_unlocked = serializers.BooleanField(required=True)
    deadline = serializers.DateTimeField(required=False, allow_null=True)
    allow_late_submission = serializers.BooleanField(required=False, default=False)
    batch_name = serializers.CharField(required=False, default='All')


class BulkModuleUnlockSerializer(serializers.Serializer):
    module_id = serializers.IntegerField(required=True)
    is_unlocked = serializers.BooleanField(required=True)
    deadline = serializers.DateTimeField(required=False, allow_null=True)


class SubmissionSubmitSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    language = serializers.CharField(required=False, default='python')
    batch_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, default='')


class TestRunSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    language = serializers.CharField(required=False, default='python')
    expected_output = serializers.CharField(required=False, allow_blank=True, default='')


class SubmissionDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.display_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    topic_title = serializers.CharField(source='problem.topic.title', read_only=True)
    course_name = serializers.CharField(source='problem.topic.module.subject.name', read_only=True)
    batch_name = serializers.CharField(source='batch.name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.display_name', read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'student', 'student_name', 'student_username',
            'problem', 'problem_title', 'topic_title', 'course_name',
            'batch', 'batch_name', 'language', 'submitted_code',
            'actual_output', 'expected_output', 'is_passed', 'status',
            'execution_time_ms', 'error_detail', 'attempt_number',
            'security_violations', 'violation_details',
            'notes', 'score', 'staff_feedback', 'submitted_at',
            'reviewed_at', 'reviewed_by', 'reviewed_by_name'
        ]
        read_only_fields = ['id', 'submitted_at', 'reviewed_at', 'reviewed_by_name']


class ReviewSubmissionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['PASSED', 'FAILED', 'REVISION_REQUESTED', 'SUBMITTED'])
    score = serializers.IntegerField(required=False, allow_null=True)
    staff_feedback = serializers.CharField(required=False, allow_blank=True)
