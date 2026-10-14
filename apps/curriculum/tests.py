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

    def test_unauthenticated_user_cannot_access_topic_detail(self):
        from .models import Subject
        subj = Subject.objects.create(name='Secure C', slug='secure-c')
        mod = Module.objects.create(subject=subj, name='Module 1', level='beginner', order=1)
        top = Topic.objects.create(module=mod, topic_id='secure-top', title='Secure Topic', order=1)

        # Unauthenticated request must be rejected
        res = self.client.get(f'/api/curriculum/topics/{top.topic_id}/')
        self.assertIn(res.status_code, [401, 403])

    def test_non_enrolled_student_forbidden_from_topic_detail(self):
        from .models import Subject
        subj = Subject.objects.create(name='Secure Java', slug='secure-java')
        mod = Module.objects.create(subject=subj, name='Module 1', level='beginner', order=1)
        top = Topic.objects.create(module=mod, topic_id='java-top', title='Java Topic', order=1)

        self.client.force_authenticate(user=self.student)
        res = self.client.get(f'/api/curriculum/topics/{top.topic_id}/')
        self.assertEqual(res.status_code, 403)
        self.assertIn('Enrollment required', str(res.data))

    def test_enrolled_student_can_access_topic_detail(self):
        from .models import Subject, CourseEnrollment
        subj = Subject.objects.create(name='Enrolled Python', slug='enrolled-python')
        mod = Module.objects.create(subject=subj, name='Module 1', level='beginner', order=1)
        top = Topic.objects.create(module=mod, topic_id='python-top', title='Python Topic', order=1)
        CourseEnrollment.objects.create(student=self.student, subject=subj, status='ACTIVE')

        self.client.force_authenticate(user=self.student)
        res = self.client.get(f'/api/curriculum/topics/{top.topic_id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['title'], 'Python Topic')

    def test_quiz_answer_keys_not_exposed_to_student(self):
        from .models import Subject, CourseEnrollment, TopicQuizQuestion
        subj = Subject.objects.create(name='Quiz Python', slug='quiz-python')
        mod = Module.objects.create(subject=subj, name='Module 1', level='beginner', order=1)
        top = Topic.objects.create(module=mod, topic_id='quiz-top', title='Quiz Topic', order=1)
        TopicQuizQuestion.objects.create(
            topic=top,
            question_text='What is Python?',
            option_a='A language',
            option_b='A snake',
            option_c='A car',
            option_d='A movie',
            correct_option='A',
            explanation='Python is a high-level programming language.'
        )
        CourseEnrollment.objects.create(student=self.student, subject=subj, status='ACTIVE')

        self.client.force_authenticate(user=self.student)
        res = self.client.get(f'/api/curriculum/topics/{top.topic_id}/')
        self.assertEqual(res.status_code, 200)
        questions = res.data.get('quiz_questions', [])
        self.assertEqual(len(questions), 1)
        # correct_option and explanation must NOT be exposed to student
        self.assertNotIn('correct_option', questions[0])
        self.assertNotIn('explanation', questions[0])

    def test_course_enrollment_and_duplicate_handling(self):
        from .models import Subject, CourseEnrollment
        subj = Subject.objects.create(name='Cloud Architecture', slug='cloud-arch')

        self.client.force_authenticate(user=self.student)
        res = self.client.post('/api/enroll/', {'subject_id': subj.id}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertTrue(res.data.get('success'))

        # Duplicate enrollment request should succeed idempotently without creating duplicate rows
        res_dup = self.client.post('/api/enroll/', {'subject_id': subj.id}, format='json')
        self.assertEqual(res_dup.status_code, 200)
        self.assertEqual(CourseEnrollment.objects.filter(student=self.student, subject=subj).count(), 1)

    def test_enrollment_with_invalid_subject_returns_404(self):
        self.client.force_authenticate(user=self.student)
        res = self.client.post('/api/enroll/', {'subject_id': 999999}, format='json')
        self.assertEqual(res.status_code, 404)

