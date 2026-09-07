import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalari_backend.settings')
django.setup()

from apps.curriculum.models import Subject, Module
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. Ensure Django Subject exists
django_sub, created = Subject.objects.get_or_create(
    slug='django',
    defaults={
        'name': 'Django Full Stack Mastery',
        'short_description': 'Zero to Hero Django web development with MVT, ORM, DRF, and real-world deployment.',
        'description': (
            'A comprehensive, industry-aligned training path designed for students starting from scratch. '
            'Covers complete Django architecture, PostgreSQL ORM queries, templates, user authentication, '
            'Django REST Framework API development, WebSockets with Channels, and production deployment on Render & Vercel.'
        ),
        'icon': 'django',
        'instructor_name': 'Prof. Deepan & Staff Team',
        'level': 'Beginner to Advanced',
        'duration': '8 Weeks (Self-Paced + Live Mentorship)',
        'order': 1,
        'is_active': True,
    }
)
print(f"Subject '{django_sub.name}' ready (created={created})")

# Link all existing unlinked modules to Django subject
unlinked = Module.objects.filter(subject__isnull=True)
count = unlinked.update(subject=django_sub)
print(f"Linked {count} existing modules to '{django_sub.name}'")

# 2. Add sample additional courses for catalog variety
python_sub, p_created = Subject.objects.get_or_create(
    slug='python-core',
    defaults={
        'name': 'Python Core & Scripting',
        'short_description': 'Master Python syntax, object-oriented programming, data structures, and automation.',
        'description': 'The fundamental bedrock for Python backend engineering. Covers control flows, OOP classes, error handling, generators, and file I/O.',
        'icon': 'python',
        'instructor_name': 'Senior Python Faculty',
        'level': 'Beginner Level',
        'duration': '4 Weeks',
        'order': 2,
        'is_active': True,
    }
)
print(f"Subject '{python_sub.name}' ready (created={p_created})")

api_sub, a_created = Subject.objects.get_or_create(
    slug='django-drf-apis',
    defaults={
        'name': 'REST APIs with Django & DRF',
        'short_description': 'Build high-performance RESTful microservices with JWT authentication, serializers, and Swagger.',
        'description': 'Enterprise API design with Django REST Framework. Covers ViewSets, nested serializers, token authentication, rate limiting, and Postman testing.',
        'icon': 'server',
        'instructor_name': 'Backend API Specialist',
        'level': 'Intermediate to Advanced',
        'duration': '5 Weeks',
        'order': 3,
        'is_active': True,
    }
)
print(f"Subject '{api_sub.name}' ready (created={a_created})")

# 3. Update staff user to Super Admin and link to Django
try:
    staff_user = User.objects.get(username='staff')
    staff_user.is_admin_role = True
    staff_user.assigned_subject = django_sub
    staff_user.save()
    print(f"Updated staff user '{staff_user.username}' as Admin with assigned subject '{django_sub.name}'")
except User.DoesNotExist:
    pass

print("Seeding subjects completed successfully!")
