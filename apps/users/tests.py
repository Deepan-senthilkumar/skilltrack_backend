from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.curriculum.models import Subject

User = get_user_model()


class StudentAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.subject = Subject.objects.create(
            name='Django Full Stack',
            slug='django',
            description='Test course'
        )

    def test_student_registration_and_pin_login(self):
        # 1. Register student with Name, Mobile, Email, and 4-digit PIN
        reg_data = {
            'name': 'Karthik Raja',
            'mobile_number': '9876543210',
            'email': 'karthik@example.com',
            'pin': '4321',
            'batch_name': 'Batch 2026'
        }
        res = self.client.post('/api/auth/student-register/', reg_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', res.data)
        self.assertEqual(res.data['user']['mobile_number'], '9876543210')
        self.assertEqual(res.data['user']['role'], 'STUDENT')

        # 2. Login using Mobile Number + PIN
        login_data = {
            'identifier': '9876543210',
            'secret': '4321'
        }
        login_res = self.client.post('/api/auth/login/', login_data, format='json')
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_res.data)
        self.assertEqual(login_res.data['user']['username'], '9876543210')
        self.assertEqual(login_res.data['user']['role'], 'STUDENT')

        # 3. Login using Email + PIN
        email_login_data = {
            'identifier': 'karthik@example.com',
            'secret': '4321'
        }
        email_res = self.client.post('/api/auth/login/', email_login_data, format='json')
        self.assertEqual(email_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', email_res.data)

    def test_admin_create_staff_member(self):
        admin_user = User.objects.create_user(
            username='admin_staff',
            email='admin@kalari.com',
            password='AdminPassword123',
            role='STAFF',
            is_admin_role=True
        )
        self.client.force_authenticate(user=admin_user)

        # Admin creates new staff instructor for Python
        staff_data = {
            'username': 'python_staff',
            'email': 'python_staff@kalari.com',
            'password': 'StaffSecret123',
            'first_name': 'Suresh Kumar',
            'assigned_subject_id': self.subject.id
        }
        res = self.client.post('/api/staff/faculty/create/', staff_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verify created user
        created_staff = User.objects.get(username='python_staff')
        self.assertEqual(created_staff.role, 'STAFF')
        self.assertEqual(created_staff.assigned_subject, self.subject)
