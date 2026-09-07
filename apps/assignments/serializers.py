from rest_framework import serializers
from .models import ProblemAccess, Submission
from apps.curriculum.models import Problem


class ProblemAccessControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemAccess
        fields = ['id', 'problem', 'is_unlocked', 'unlocked_at', 'deadline', 'allow_late_submission', 'batch_name']
        read_only_fields = ['id']


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
    submitted_code = serializers.CharField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class SubmissionDetailSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    student_batch = serializers.CharField(source='student.batch_name', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    topic_title = serializers.CharField(source='problem.topic.title', read_only=True)
    module_name = serializers.CharField(source='problem.topic.module.name', read_only=True)
    max_points = serializers.IntegerField(source='problem.points', read_only=True)
    reviewer_username = serializers.CharField(source='reviewed_by.username', read_only=True, allow_null=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'student', 'student_username', 'student_email', 'student_batch',
            'problem', 'problem_title', 'topic_title', 'module_name', 'max_points',
            'submitted_code', 'notes', 'status', 'score', 'staff_feedback',
            'is_late', 'submitted_at', 'reviewed_at', 'reviewer_username'
        ]
        read_only_fields = ['id', 'student', 'submitted_at', 'reviewed_at', 'reviewer_username']


class ReviewSubmissionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['PASSED', 'REVISION_REQUESTED', 'REJECTED'])
    score = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    staff_feedback = serializers.CharField(required=False, allow_blank=True, default="")
