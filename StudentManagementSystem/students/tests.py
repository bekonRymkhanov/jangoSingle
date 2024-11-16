from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from students.models import Student
import time

class StudentModelTest(TestCase):
    def setUp(self):
        # Create a user for the student
        user = User.objects.create_user(
            email="student@kbtu.kz",
            username="student_user",
            password="password",
            role="admin"
        )
        self.student_data = {
            'user': user,
            'student_id': 12345,
            'name': 'John Doe',
            'dob': '2000-01-01'
        }

    def test_student_creation(self):
        student = Student.objects.create(**self.student_data)
        self.assertEqual(student.student_id, 12345)
        self.assertEqual(student.name, 'John Doe')
        self.assertEqual(student.user.email, 'student@kbtu.kz')

class StudentSerializerTest(APITestCase):
    def setUp(self):
        # Create users for authentication
        self.admin_user = User.objects.create_user(
            email="admin@gmail.com",
            username="beka",
            password="beka2004",
            role="admin"
        )
        self.student_user = User.objects.create_user(
            email="student@kbtu.kz",
            username="student_user",
            password="student_password",
            role="student"
        )

        # Authenticate as the admin user
        self.client.force_authenticate(user=self.admin_user)

        # Student data for creation
        self.student_data = {
            'user_id': self.student_user.id,
            'student_id': 12345,
            'name': 'John Doe',
            'dob': '2000-01-01'
        }

        self.url = reverse('student-list')  # URL for the student list view

    def test_create_student(self):
        # Create student using POST request
        response = self.client.post(self.url, self.student_data, format='json')

        # Assert successful creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student_id'], 12345)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_create_student_missing_student_id(self):
        data = self.student_data.copy()
        data.pop('student_id')  # Remove student_id to test required field validation

        # Create student with missing student_id
        response = self.client.post(self.url, data, format='json')

        # Assert missing student_id raises a 400 error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("student_id", response.data)

    def test_update_student(self):
        # Create student instance
        student = Student.objects.create(
            user=self.student_user,
            student_id=12346,
            name="Jane Doe",
            dob="2000-01-01"
        )

        # URL for updating the student instance
        url = reverse('student-detail', args=[student.id])

        # Data for updating the student
        updated_data = {
            'student_id': 67890,
            'name': 'Jane Smith'
        }

        # Update student using PATCH request
        response = self.client.patch(url, updated_data, format='json')

        # Assert successful update and correct response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], 67890)
        self.assertEqual(response.data['name'], 'Jane Smith')

    def test_update_student_with_user_id(self):
        # Create student instance
        student = Student.objects.create(
            user=self.student_user,
            student_id=12347,
            name="James Doe",
            dob="2000-01-01"
        )

        # URL for updating the student instance
        url = reverse('student-detail', args=[student.id])

        # Data for updating with user_id (which is not allowed)
        updated_data = {
            'user_id': 99999  # Trying to change user_id, which should be disallowed
        }

        # Update student using PATCH request
        response = self.client.patch(url, updated_data, format='json')

        # Assert error due to disallowed user_id update
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user_id", response.data)

class StudentPermissionsTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email='admin@kbtu.kz', username='admin', password='password', role='admin'
        )
        self.student_user = User.objects.create_user(
            email='student@kbtu.kz', username='student', password='password', role='student'
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_can_create_student(self):
        url = reverse('student-list')
        data = {
            'user_id': self.student_user.id,
            'student_id': 12345,
            'name': 'John Doe',
            'dob': '2000-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_student(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('student-list')
        data = {
            'user_id': self.student_user.id,
            'student_id': 12345,
            'name': 'John Doe',
            'dob': '2000-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentCacheTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='student@kbtu.kz', username='student', password='password', role='student'
        )
        self.student = Student.objects.create(
            user=self.user, student_id=12345, name="John Doe", dob="2000-01-01"
        )
        self.url = reverse('student-list')

    def test_cache_used_for_multiple_requests(self):
        # Check the time for the first request
        start_time = time.time()
        self.client.get(self.url)
        first_request_time = time.time() - start_time

        # Check the time for the second request (should be faster due to caching)
        start_time = time.time()
        self.client.get(self.url)
        second_request_time = time.time() - start_time

        self.assertTrue(second_request_time < first_request_time)

