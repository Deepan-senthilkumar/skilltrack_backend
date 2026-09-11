from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.curriculum.models import Problem, Batch


class ProblemAccess(models.Model):
    objects = models.Manager()
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, related_name='access_control')
    is_unlocked = models.BooleanField(default=False, help_text="Toggles whether problem is visible to students")
    unlocked_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    allow_late_submission = models.BooleanField(default=True)
    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.SET_NULL, related_name='problem_access_controls')
    batch_name = models.CharField(max_length=100, default='All')

    class Meta:
        verbose_name = "Problem Access Control"
        verbose_name_plural = "Problem Access Controls"

    @property
    def is_active_now(self):
        if not self.is_unlocked:
            return False
        if self.deadline and timezone.now() > self.deadline and not self.allow_late_submission:
            return False
        return True

    def __str__(self):
        status = "UNLOCKED" if self.is_unlocked else "LOCKED"
        return f"{self.problem.title} [{status}]"


class Submission(models.Model):
    objects = models.Manager()
    STATUS_CHOICES = (
        ('PASSED', 'Passed / Correct'),
        ('FAILED', 'Incorrect Output'),
        ('COMPILE_ERROR', 'Compilation Error'),
        ('RUNTIME_ERROR', 'Runtime Error'),
        ('TIMEOUT', 'Execution Timeout'),
        ('FAILED_SECURITY', 'Terminated - Security Violation'),
        ('SUBMITTED', 'Submitted - Pending Review'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.SET_NULL, related_name='submissions')
    language = models.CharField(max_length=20, default='python')
    submitted_code = models.TextField(help_text="Student's submitted code")
    actual_output = models.TextField(blank=True, default="", help_text="Captured console output from execution")
    expected_output = models.TextField(blank=True, default="", help_text="Target expected output key")
    is_passed = models.BooleanField(default=False)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='SUBMITTED')
    execution_time_ms = models.FloatField(default=0.0, help_text="Execution duration in milliseconds")
    error_detail = models.TextField(blank=True, default="", help_text="Full compiler or runtime trace")
    attempt_number = models.PositiveIntegerField(default=1)
    security_violations = models.PositiveIntegerField(default=0, help_text="Security tab switch or devtools infractions")
    violation_details = models.TextField(blank=True, default="", help_text="Security infraction logs")
    notes = models.TextField(blank=True, default="", help_text="Student comments or notes")
    score = models.PositiveIntegerField(null=True, blank=True)
    staff_feedback = models.TextField(blank=True, default="")
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_submissions'
    )

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        status_label = "PASS" if self.is_passed else self.status
        return f"{self.student.username} -> {self.problem.title} [{status_label}] (Attempt #{self.attempt_number})"
