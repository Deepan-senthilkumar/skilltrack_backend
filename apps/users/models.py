from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin / Owner'),
        ('STAFF', 'Staff / Trainer'),
        ('STUDENT', 'Student / Learner'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    mobile_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    pin_code = models.CharField(max_length=10, blank=True, default='')
    assigned_subject = models.ForeignKey(
        'curriculum.Subject',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_staff_users'
    )
    is_admin_role = models.BooleanField(default=False)
    batch_name = models.CharField(max_length=100, blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')
    bio = models.TextField(blank=True, default='')
    is_active_account = models.BooleanField(default=True)

    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser or self.is_admin_role

    @property
    def is_instructor(self):
        return self.role in ['ADMIN', 'STAFF'] or self.is_staff or self.is_superuser or self.is_admin_role

    @property
    def is_student(self):
        return self.role == 'STUDENT'

    @property
    def display_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username

    def __str__(self):
        return f"{self.username} [{self.role}]"
