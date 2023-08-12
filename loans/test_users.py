from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
import json

class UserViewsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    # Test 1: Retrieve and Create Users
    def test_user_list_create_view(self):
        # Test GET request to retrieve users
        response = self.client.get(reverse("user_list_create_view"))  # Updated view name
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 2: Retrieve User Details
    def test_user_detail_view(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # Test GET request to retrieve user details
        response = self.client.get(reverse("user_detail_view", args=[user.pk]))  # Updated view name
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 3: User Login
    def test_user_login(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # Test POST request for user login
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse("user_login"), login_data, format='json')  # Updated view name
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test 4: Create User with Minimum Field Length
    def test_create_user_with_minimum_fields(self):
        user_data = {
            'username': 'u',
            'email': 'u@example.com',
            'password': 'pass'
        }
        response = self.client.post(reverse("user_list_create_view"), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #Test 5: Create User with Maximum Field Length
    def test_create_user_with_maximum_fields(self):
        user_data = {
            'username': 'u' * 30,
            'email': 'u' * 50 + '@example.com',
            'password': 'p' * 128  # Maximum password length
        }
        response = self.client.post(reverse("user_list_create_view"), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    #Test 6: Create User with Invalid Data
    def test_create_user_with_invalid_data(self):
        user_data = {
            'username': '',
            'email': 'invalid_email',  # Invalid email format
            'password': 'short'  # Too short password
        }
        response = self.client.post(reverse("user_list_create_view"), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    #Test 7: Update User Details
    def test_update_user_details(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        updated_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }
        response = self.client.put(reverse("user_detail_view", args=[user.pk]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test 8: Update Non-existing User
    def test_update_non_existing_user(self):
        response = self.client.put(reverse("user_detail_view", args=[999]), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    #Test 9: Delete User
    def test_delete_user(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        response = self.client.delete(reverse("user_detail_view", args=[user.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #Test 10: Delete Non-existing User
    def test_delete_non_existing_user(self):
        response = self.client.delete(reverse("user_detail_view", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        



