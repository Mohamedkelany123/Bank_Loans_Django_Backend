from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from loans.models import LoanFund, Loan
from decimal import Decimal

class LoanViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a LoanFund object
        self.loanfund = LoanFund.objects.create(
            name='Test Fund',
            amount=50000,
            max_loan_amount=50000,
            min_loan_amount=150,
            interest_rate=0.01,
            loan_duration=2
        )

    # Test 1: Create a valid loan
    def test_create_valid_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test 2: Create a loan with invalid loan_fund_id
    def test_create_invalid_loan_fund_id(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': 999,  # Non-existent loan fund ID
            'amount': 1000,
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # Test 3: Create a loan with amount exceeding fund
    def test_create_loan_amount_exceeds_fund(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 60000,  # Exceeds loan fund amount
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # Test 4: Create a loan with amount below min loan amount
    def test_create_loan_amount_below_min_amount(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 100,  # Below min loan amount
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 5: Approve a loan
    def test_approve_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = response.data['id']  # Assuming your API response includes the created loan's ID

        response = self.client.put(reverse("approve_loan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Loan.objects.get(pk=loan_id).status, 'Approved')


    # Test 6: Reject a loan
    def test_reject_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = response.data['id']  # Assuming your API response includes the created loan's ID

        response = self.client.put(reverse("reject_loan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Loan.objects.get(pk=loan_id).status, 'Rejected')
        

    # Test 7: Delete a loan
    def test_delete_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = response.data['id']  # Assuming your API response includes the created loan's ID

        response = self.client.delete(reverse("deleteLoan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Loan.objects.filter(pk=loan_id).exists())



    # Test 8: Retrieve loans by username
    def test_get_loans_by_username(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("get_loans_by_username", args=['John Doe']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customerName'], 'John Doe')


    # Test 9: Retrieve all loans
    def test_get_all_loans(self):
        # Create multiple loans using the loan_list_create_view API
        data1 = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        response1 = self.client.post(reverse("loan_list_create_view"), data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        data2 = {
            'customerName': 'Jane Smith',
            'loan_fund_id': self.loanfund.pk,
            'amount': 2000,
            'status': 'Requested',
        }
        response2 = self.client.post(reverse("loan_list_create_view"), data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Retrieve all loans
        response = self.client.get(reverse("loan_list_create_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming the above created 2 loans



