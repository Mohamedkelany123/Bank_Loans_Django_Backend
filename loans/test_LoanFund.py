from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from loans.models import LoanFund
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class LoanFundViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

#-------------------------------------------------------------------------------------------------#

    # Test 1.1: Retrieve all loan funds
    def test_retrieve_all_loan_funds(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse("loanfund_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 1.2: Create a new loan fund with valid data
    def test_create_valid_loan_fund(self):
        data = {
            'name': 'Test Fund',
            'amount': 10000,
            'max_loan_amount': 50000,
            'min_loan_amount': 1000,
            'interest_rate': 4,
            'loan_duration': 12
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test 1.3: Create a new loan fund with invalid numeric data
    def test_create_invalid_loan_fund(self):
        data = {
            'name': 'Test Fund',
            'amount': 'invalid',
            'max_loan_amount': -50000,
            'min_loan_amount': 'invalid',
            'interest_rate': 'invalid',
            'loan_duration': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

     # Test 1.4: Attempt to create a loan fund with negative interest rate
    def test_create_loan_fund_negative_interest_rate(self):
        data = {
            'name': 'Negative Interest Fund',
            'amount': 10000,
            'max_loan_amount': 50000,
            'min_loan_amount': 1000,
            'interest_rate': -4,  # Negative interest rate
            'loan_duration': 12
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 1.5: Attempt to create a loan fund with loan duration less than 2
    def test_create_loan_fund_invalid_loan_duration(self):
        data = {
            'name': 'Invalid Loan Duration Fund',
            'amount': 10000,
            'max_loan_amount': 50000,
            'min_loan_amount': 1000,
            'interest_rate': 4,
            'loan_duration': 0  # Invalid duration
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 1.6: Create a loan fund with decimal values
    def test_create_loan_fund_decimal_values(self):
        data = {
            'name': 'Decimal Fund',
            'amount': 1234.56,  # Decimal value
            'max_loan_amount': 5000.75,
            'min_loan_amount': 200.50,
            'interest_rate': 2.75,
            'loan_duration': 24
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test 1.7: Create a loan fund with Max is less than Min
    def test_invalid_max_loan_amount_message(self):
        invalid_data = {
            "name": "Invalid Fund",
            "amount": 100,
            "max_loan_amount": 9,  # Invalid max
            "min_loan_amount": 10,
            "interest_rate": 5.0,
            "loan_duration": 12,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse('loanfund_list')  , data=invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 1.7: Create a loan fund with Min is equal Max
    def test_valid_max_loan_amount_message(self):
        data = {
            "name": "Invalid Fund",
            "amount": 100,
            "max_loan_amount": 10,  
            "min_loan_amount": 10,
            "interest_rate": 5.0,
            "loan_duration": 12,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#-------------------------------------------------------------------------------------------------#


    # Test 2.1: Retrieve loan fund details by ID
    def test_retrieve_loan_fund_details(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        response = self.client.get(reverse("loanfund_detail", args=[loanfund.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 2.2: Update loan fund amount by adding a valid entered amount
    def test_update_loan_fund_amount(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 2000}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 2.3: Update loan fund amount with an invalid entered amount
    def test_update_invalid_loan_fund_amount(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 'invalid'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 2.4: Delete loan fund by ID
    def test_delete_loan_fund(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(reverse("loanfund_detail", args=[loanfund.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test 2.5: Attempt to retrieve non-existent loan fund details
    def test_retrieve_non_existent_loan_fund(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse("loanfund_detail", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test 2.6: Update loan fund amount to exceed max allowed value
    def test_update_loan_fund_amount_exceeding_max(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 9999999999}  # Exceeds maximum value
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # Test 2.7: Delete non-existent loan fund
    def test_delete_non_existent_loan_fund(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(reverse("loanfund_detail", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test 2.8: Update loan fund amount with an invalid entered amount
    def test_update_zero_loan_fund_amount(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 0}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 2.9: Update loan fund amount with an invalid negative entered amount
    def test_update_negative_loan_fund_amount(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': -100}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

   
#-------------------------------------------------------------------------------------------------#
    
        