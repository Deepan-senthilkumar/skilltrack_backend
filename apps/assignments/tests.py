from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from apps.curriculum.models import Module, Topic, Problem
from apps.assignments.models import ProblemAccess, Submission

User = get_user_model()


class TimelineAndAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.staff = User.objects.create_user(
            username='teststaff',
            password='Password@123',
            role='STAFF',
            is_staff=True
        )

        self.student = User.objects.create_user(
            username='teststudent',
            password='Password@123',
            role='STUDENT'
        )

        self.module = Module.objects.create(name='Test Module', level='beginner', order=1)
        self.topic = Topic.objects.create(
            module=self.module,
            topic_id='test-topic',
            title='Test Topic',
            explain=['Test paragraph'],
            order=1
        )
        self.problem = Problem.objects.create(
            topic=self.topic,
            title='Sample Challenge',
            description='Write a django view with HttpResponse',
            points=10,
            order=1
        )
        self.access = ProblemAccess.objects.create(
            problem=self.problem,
            is_unlocked=False
        )

    def test_student_cannot_submit_to_locked_problem(self):
        self.client.force_authenticate(user=self.student)
        url = f'/api/problems/{self.problem.id}/submit/'
        resp = self.client.post(url, {'submitted_code': 'def test(): pass'})
        self.assertEqual(resp.status_code, 403)
        self.assertIn('not been unlocked', resp.data['detail'])

    def test_student_cannot_submit_after_expired_deadline(self):
        self.access.is_unlocked = True
        self.access.deadline = timezone.now() - timedelta(minutes=10)  # expired!
        self.access.save()

        self.client.force_authenticate(user=self.student)
        url = f'/api/problems/{self.problem.id}/submit/'
        resp = self.client.post(url, {'submitted_code': 'def test(): pass'})
        self.assertEqual(resp.status_code, 403)
        self.assertIn('deadline', resp.data['detail'])

    def test_student_auto_grading_within_deadline(self):
        self.access.is_unlocked = True
        self.access.deadline = timezone.now() + timedelta(hours=2)  # active!
        self.access.save()

        self.client.force_authenticate(user=self.student)
        url = f'/api/problems/{self.problem.id}/submit/'
        resp = self.client.post(url, {
            'submitted_code': 'from django.http import HttpResponse\ndef my_view(req): return HttpResponse("ok")',
            'notes': '200 OK returned successfully'
        })
        self.assertEqual(resp.status_code, 200)
        # Automatic grading should have passed it!
        self.assertEqual(resp.data['status'], 'PASSED')
        self.assertGreaterEqual(resp.data['score'], 6)
        self.assertIn('Auto-Graded', resp.data['staff_feedback'])

        # Verify in DB
        sub = Submission.objects.get(student=self.student, problem=self.problem)
        self.assertEqual(sub.status, 'PASSED')

    def test_student_test_run_endpoint(self):
        self.client.force_authenticate(user=self.student)
        url = f'/api/problems/{self.problem.id}/test-run/'
        resp = self.client.post(url, {
            'submitted_code': 'from django.http import HttpResponse\ndef my_view(req): return HttpResponse("ok")',
            'notes': 'test output'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn('tests', resp.data)
        self.assertGreaterEqual(resp.data['score'], 6)

    def test_staff_can_review_and_grade_submission(self):
        # Setup active submission
        self.access.is_unlocked = True
        self.access.save()
        sub = Submission.objects.create(
            student=self.student,
            problem=self.problem,
            submitted_code='code test',
            status='SUBMITTED'
        )

        self.client.force_authenticate(user=self.staff)
        url = f'/api/staff/submissions/{sub.id}/review/'
        resp = self.client.post(url, {
            'status': 'PASSED',
            'score': 10,
            'staff_feedback': 'Excellent work!'
        })
        self.assertEqual(resp.status_code, 200)
        sub.refresh_from_db()
        self.assertEqual(sub.status, 'PASSED')
        self.assertEqual(sub.score, 10)
        self.assertEqual(sub.staff_feedback, 'Excellent work!')
