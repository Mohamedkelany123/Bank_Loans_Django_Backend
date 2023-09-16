from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from loans.models import LoanFund, Loan
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class LoanViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)


        # Create a LoanFund object
        self.loanfund = LoanFund.objects.create(
            name='Test Fund',
            amount=50000,
            max_loan_amount=50000,
            min_loan_amount=150,    
            interest_rate=0.01,
            loan_duration=2
        )


#--------------------------------------------------------------------------------------------------#

       

    # Test 1.1: Create a valid loan
    def test_create_valid_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test 1.2: Create a loan with invalid loan_fund_id
    def test_create_invalid_loan_fund_id(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': 999,  # Non-existent loan fund ID
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test 1.3: Create loan Without Providing LoanFund ID
    def test_create_loan_without_loan_fund_id(self):
        loan_data = {
            'customerName': 'John Doe',
            'amount': 1000,
            'status': 'Requested',
            #no LoanFundID
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), loan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('loan_fund_id must be provided.', response.data['error'])


    # Test 1.4: Create a loan with amount exceeding fund
    def test_create_loan_amount_exceeds_fund(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 60000,  # Exceeds loan fund amount
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




    # Test 1.5: Create a loan with amount below min loan amount
    def test_create_loan_amount_below_min_amount(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 100,  # Below min loan amount
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    # Test 1.6: Create 2 Loans with same loanFund ID Then Get Them
    def test_get_all_loans(self):
        # Create multiple loans using the loan_list_create_view API
        data1 = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response1 = self.client.post(reverse("loan_list_create_view"), data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        data2 = {
            'customerName': 'Jane Smith',
            'loan_fund_id': self.loanfund.pk,
            'amount': 2000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response2 = self.client.post(reverse("loan_list_create_view"), data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Retrieve all loans
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse("loan_list_create_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

#--------------------------------------------------------------------------------------------------#


    # Test 2.1: Approve a loan
    def test_approve_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = response.data['id']  # Assuming your API response includes the created loan's ID

        response = self.client.put(reverse("approve_loan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Loan.objects.get(pk=loan_id).status, 'Approved')

    # Test 2.2: Approve a loan with wrong LoanFundID
    def test_approve_nonexistent_loan(self):
        loan_id = 999  # An ID that does not exist in the database
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("approve_loan", args=[loan_id]), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Loan with the provided id does not exist.'})

#--------------------------------------------------------------------------------------------------#


    # Test 3.1: Reject a loan
    def test_reject_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = response.data['id']  

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("reject_loan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Loan.objects.get(pk=loan_id).status, 'Rejected')

    # Test 3.2: Reject a loan with wrong LoanFundID
    def test_reject_nonexistent_loan(self):
        loan_id = 999  # Invalid ID

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(reverse("reject_loan", args=[loan_id]), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Loan with the provided id does not exist.'})
        
#--------------------------------------------------------------------------------------------------#

    # Test 4.1: Delete a loan
    def test_delete_loan(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = response.data['id'] 
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(reverse("deleteLoan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Loan.objects.filter(pk=loan_id).exists())

    # Test 4.2: Delete a loan with wrong loanID
    def test_delete_loan_wrongID(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        loan_id = 999

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(reverse("deleteLoan", args=[loan_id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Loan with the provided id does not exist.'})

#--------------------------------------------------------------------------------------------------#

    # Test 5.1: Retrieve loans by username
    def test_get_loans_by_username(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse("get_loans_by_username", args=['John Doe']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customerName'], 'John Doe')

    # Test 5.2: Retrieve loans by wrong username
    def test_get_loans_by_wrong_username(self):
        data = {
            'customerName': 'John Doe',
            'loan_fund_id': self.loanfund.pk,
            'amount': 1000,
            'status': 'Requested',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(reverse("loan_list_create_view"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(reverse("get_loans_by_username", args=['Steve']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

#--------------------------------------------------------------------------------------------------#





