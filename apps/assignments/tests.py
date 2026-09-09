from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from apps.curriculum.models import Subject, Module, Topic, Problem, Batch, BatchTopicProgress, StaffDailyLog
from apps.assignments.models import ProblemAccess, Submission

User = get_user_model()


class SkillStackPlatformTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='testadmin',
            password='Password@123',
            role='ADMIN',
            is_staff=True,
            is_superuser=True
        )

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

        self.course = Subject.objects.create(
            name='C Programming',
            slug='c-programming',
            duration='6 Weeks',
            schedule_type='3 days class + 3 days lab'
        )

        self.module = Module.objects.create(
            subject=self.course,
            name='Module 1',
            level='beginner',
            order=1
        )

        self.topic = Topic.objects.create(
            module=self.module,
            topic_id='c-syntax',
            title='Variables in C',
            order=1
        )

        self.problem = Problem.objects.create(
            topic=self.topic,
            title='Sample Print Program',
            description='Print hello world',
            language='python',
            expected_output='Hello World',
            points=10,
            order=1
        )

        self.batch = Batch.objects.create(
            name='C Programming - Morning Batch A',
            course=self.course,
            schedule='Mon-Wed-Fri 10:00 AM',
            status='ACTIVE'
        )
        self.batch.staff.add(self.staff)
        self.batch.students.add(self.student)

    def test_duplicate_course_name_in_distinct_batches(self):
        # A second batch with same course name
        batch_b = Batch.objects.create(
            name='C Programming - Evening Batch B',
            course=self.course,
            schedule='Tue-Thu-Sat 03:00 PM',
            status='ACTIVE'
        )
        self.assertEqual(batch_b.course.name, self.batch.course.name)
        self.assertNotEqual(batch_b.id, self.batch.id)

    def test_sandboxed_code_execution_and_auto_validation(self):
        self.client.force_authenticate(user=self.student)
        url = f'/api/problems/{self.problem.id}/submit/'
        resp = self.client.post(url, {
            'code': 'print("Hello World")',
            'language': 'python',
            'batch_id': self.batch.id
        })
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data['is_passed'])
        self.assertEqual(resp.data['status'], 'PASSED')
        self.assertEqual(resp.data['actual_output'].strip(), 'Hello World')
        self.assertGreater(resp.data['execution_time_ms'], 0)

    def test_topic_progress_independent_of_attendance(self):
        self.client.force_authenticate(user=self.staff)
        toggle_url = f'/api/batches/{self.batch.id}/topics/{self.topic.id}/toggle/'
        resp = self.client.post(toggle_url, {'is_completed': True, 'remarks': 'Completed today'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['is_completed'])
        self.assertEqual(resp.data['remarks'], 'Completed today')

    def test_staff_daily_session_log(self):
        self.client.force_authenticate(user=self.staff)
        url = '/api/staff-logs/'
        resp = self.client.post(url, {
            'batch': self.batch.id,
            'session_type': 'TOPIC',
            'session_title': 'Variables & Data Types',
            'total_enrolled': 1,
            'students_attended': 1,
            'remarks': 'All learners present and engaged.'
        })
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['students_attended'], 1)
