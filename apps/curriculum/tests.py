from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Module, Topic, Problem
from apps.assignments.models import ProblemAccess

User = get_user_model()


class CurriculumCrudTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.staff = User.objects.create_user(
            username='crudstaff',
            password='Password@123',
            role='STAFF',
            is_staff=True
        )

        self.student = User.objects.create_user(
            username='crudstudent',
            password='Password@123',
            role='STUDENT'
        )

    def test_staff_can_create_and_delete_module(self):
        self.client.force_authenticate(user=self.staff)
        
        # Create module
        res = self.client.post('/api/staff/modules/', {
            'name': 'New Advanced Async Module',
            'level': 'advanced',
            'order': 8
        })
        self.assertEqual(res.status_code, 201)
        module_id = res.data['id']
        self.assertTrue(Module.objects.filter(id=module_id).exists())

        # Update module
        res = self.client.put(f'/api/staff/modules/{module_id}/', {
            'name': 'Updated Advanced Async Module',
            'level': 'advanced',
            'order': 9
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], 'Updated Advanced Async Module')

        # Delete module
        res = self.client.delete(f'/api/staff/modules/{module_id}/')
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Module.objects.filter(id=module_id).exists())

    def test_student_forbidden_from_creating_module(self):
        self.client.force_authenticate(user=self.student)
        res = self.client.post('/api/staff/modules/', {
            'name': 'Hacker Module',
            'level': 'beginner',
            'order': 1
        })
        self.assertEqual(res.status_code, 403)

    def test_staff_create_problem_auto_creates_access(self):
        self.client.force_authenticate(user=self.staff)
        
        mod = Module.objects.create(name='Test Mod', level='beginner', order=1)
        top = Topic.objects.create(module=mod, topic_id='test-top', title='Test Top', explain=[], order=1)

        res = self.client.post('/api/staff/problems/', {
            'topic': top.id,
            'title': 'New Challenge #1',
            'description': 'Write a template tag',
            'points': 15,
            'order': 1
        })
        self.assertEqual(res.status_code, 201)
        problem_id = res.data['id']

        # Verify ProblemAccess was auto-initialized
        access = ProblemAccess.objects.filter(problem_id=problem_id).first()
        self.assertIsNotNone(access)
        self.assertFalse(access.is_unlocked)
