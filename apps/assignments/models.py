from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.curriculum.models import Problem


class ProblemAccess(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, related_name='access_control')
    is_unlocked = models.BooleanField(default=False, help_text="Staff toggles this to make problem accessible to students")
    unlocked_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True, help_text="Timestamp after which students can no longer submit")
    allow_late_submission = models.BooleanField(default=False)
    batch_name = models.CharField(max_length=100, default='All')

    class Meta:
        verbose_name = "Problem Access & Timeline"
        verbose_name_plural = "Problem Access Controls"

    @property
    def is_active_now(self):
        if not self.is_unlocked:
            return False
        if self.deadline and timezone.now() > self.deadline:
            return False
        return True

    @property
    def is_expired(self):
        return bool(self.deadline and timezone.now() > self.deadline)

    @property
    def seconds_remaining(self):
        if not self.deadline:
            return None
        now = timezone.now()
        if now >= self.deadline:
            return 0
        return int((self.deadline - now).total_seconds())

    def __str__(self):
        status = "UNLOCKED" if self.is_unlocked else "LOCKED"
        return f"{self.problem.title} [{status}] (Deadline: {self.deadline})"


class Submission(models.Model):
    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted - Pending Review'),
        ('PASSED', 'Approved / Passed'),
        ('REVISION_REQUESTED', 'Revision Requested'),
        ('REJECTED', 'Rejected'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    submitted_code = models.TextField(help_text="Student's submitted code or answers")
    notes = models.TextField(blank=True, default="", help_text="Optional student execution log or comments")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='SUBMITTED')
    score = models.PositiveIntegerField(null=True, blank=True)
    staff_feedback = models.TextField(blank=True, default="")
    is_late = models.BooleanField(default=False)
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
        unique_together = ('student', 'problem')

    def __str__(self):
        return f"{self.student.username} -> {self.problem.title} ({self.status})"
