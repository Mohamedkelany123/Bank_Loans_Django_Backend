from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from rest_framework.authtoken.models import Token

class UserViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tokenuser', email='token@example.com', password='tokenpassword')
        self.token = Token.objects.create(user=self.user)

#------------------------------------------------------------------------------------------------------#
    #Test 1.1: Create User
    def test_create_user(self):

        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }

        response = self.client.post(reverse("user_list_create_view"), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #Test 1.2: Create Invalid User
    def test_create_user_with_invalid_data(self):
        
        invalid_user_data = {}
        response = self.client.post(reverse("user_list_create_view"), invalid_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #Test 1.3: Get Users
    def test_get_users(self):
        User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        User.objects.create_user(username='user2', email='user2@example.com', password='password2')


        response = self.client.get(reverse("user_list_create_view"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 3) 

        self.assertEqual(response.data[1]['username'], 'user1')
        self.assertEqual(response.data[2]['username'], 'user2')
    
#------------------------------------------------------------------------------------------------------#
    
    # Test 2.1: Retrieve User Details By ID
    def test_user_detail_view(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    
        # Test GET request to retrieve user details
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse("user_detail_view", args=[user.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test 2.2: Update User Details
    def test_update_user_details(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        updated_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("user_detail_view", args=[user.pk]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test 2.3: Update Non-existing User
    def test_update_non_existing_user(self):

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("user_detail_view", args=[999]), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    #Test 2.4: Delete User
    def test_delete_user(self):
        # Create a user for testing
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(reverse("user_detail_view", args=[user.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #Test 2.5: Delete Non-existing User
    def test_delete_non_existing_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(reverse("user_detail_view", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #------------------------------------------------------------------------------------------------------#

    
    # Test 3.1: User Login
    def test_user_login(self):
        # Create a user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse("user_login"), login_data, format='json')  # Updated view name
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 3.2: User Invalid Login
    def test_invalid_login(self):
        # Create a user
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'  # Wrong Password
        }
        response = self.client.post(reverse("user_login"), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


    # Test 3.3: User Invalid Login (missing username, missing password)
    def test_missing_username_or_password(self):
        
        #Missing Username
        login_data = {
            'password': 'testpassword'
        }
        response = self.client.post(reverse("user_login"), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

        # Missing Password
        login_data = {
            'username': 'testuser'
        }
        response = self.client.post(reverse("user_login"), login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)



    # Test 3.4: Invalid Requests
    def test_method_not_allowed(self):
        # Test GET request
        response = self.client.get(reverse("user_login"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test PUT request
        response = self.client.put(reverse("user_login"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test DELETE request
        response = self.client.delete(reverse("user_login"))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

# #------------------------------------------------------------------------------------------------------#