from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from loans.models import LoanFund

class LoanFundViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
    # Test 1: Retrieve all loan funds
    def test_retrieve_all_loan_funds(self):
        response = self.client.get(reverse("loanfund_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 2: Create a new loan fund with valid data
    def test_create_valid_loan_fund(self):
        data = {
            'name': 'Test Fund',
            'amount': 10000,
            'max_loan_amount': 50000,
            'min_loan_amount': 1000,
            'interest_rate': 4,
            'loan_duration': 12
        }
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test 3: Create a new loan fund with invalid numeric data
    def test_create_invalid_loan_fund(self):
        data = {
            'name': 'Test Fund',
            'amount': 'invalid',
            'max_loan_amount': -50000,
            'min_loan_amount': 'invalid',
            'interest_rate': 'invalid',
            'loan_duration': 1
        }
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 4: Retrieve loan fund details by ID
    def test_retrieve_loan_fund_details(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        response = self.client.get(reverse("loanfund_detail", args=[loanfund.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 5: Update loan fund amount by adding a valid entered amount
    def test_update_loan_fund_amount(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 2000}
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test 6: Update loan fund amount with an invalid entered amount
    def test_update_invalid_loan_fund_amount(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 'invalid'}
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 7: Delete loan fund by ID
    def test_delete_loan_fund(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        response = self.client.delete(reverse("loanfund_detail", args=[loanfund.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test 8: Attempt to retrieve non-existent loan fund details
    def test_retrieve_non_existent_loan_fund(self):
        response = self.client.get(reverse("loanfund_detail", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test 9: Update loan fund amount to exceed max allowed value
    def test_update_loan_fund_amount_exceeding_max(self):
        loanfund = LoanFund.objects.create(name='Test Fund', amount=10000, max_loan_amount=50000, min_loan_amount=1000, interest_rate=4, loan_duration=12)
        data = {'amount': 9999999999}  # Exceeds maximum value
        response = self.client.put(reverse("loanfund_detail", args=[loanfund.pk]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # Test 10: Delete non-existent loan fund
    def test_delete_non_existent_loan_fund(self):
        response = self.client.delete(reverse("loanfund_detail", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test 11: Attempt to create a loan fund with negative interest rate
    def test_create_loan_fund_negative_interest_rate(self):
        data = {
            'name': 'Negative Interest Fund',
            'amount': 10000,
            'max_loan_amount': 50000,
            'min_loan_amount': 1000,
            'interest_rate': -4,  # Negative interest rate
            'loan_duration': 12
        }
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 12: Attempt to create a loan fund with loan duration less than 2
    def test_create_loan_fund_invalid_loan_duration(self):
        data = {
            'name': 'Invalid Loan Duration Fund',
            'amount': 10000,
            'max_loan_amount': 50000,
            'min_loan_amount': 1000,
            'interest_rate': 4,
            'loan_duration': 1  # Invalid duration
        }
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 13: Create a loan fund with decimal values
    def test_create_loan_fund_decimal_values(self):
        data = {
            'name': 'Decimal Fund',
            'amount': 1234.56,  # Decimal value
            'max_loan_amount': 5000.75,
            'min_loan_amount': 200.50,
            'interest_rate': 2.75,
            'loan_duration': 24
        }
        response = self.client.post(reverse("loanfund_list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        