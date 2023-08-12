from django.test import TestCase
from decimal import Decimal
from .models import LoanFund, Loan
from django.core.exceptions import ValidationError


class ModelsTestCase(TestCase):

    # Test Case 1: Test LoanFund model string representation
    def test_loanfund_model(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 1',
            amount=1000,
            max_loan_amount=5000,
            min_loan_amount=100,
            interest_rate=5,
            loan_duration=12
        )
        self.assertEqual(str(loan_fund), 'Fund 1')

    # Test Case 2: Test Loan model string representation and monthly installment calculation
    def test_loan_model(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 2',
            amount=5000,
            max_loan_amount=10000,
            min_loan_amount=200,
            interest_rate=3,
            loan_duration=6
        )
        loan = Loan.objects.create(
            customerName='Alice',
            loan_fund_ID=loan_fund,
            loan_amount=2000,
            interest_rate=3,
            duration=6,
            status='Requested'
        )

        expected_str = 'Alice - Fund 2 - 2000'
        self.assertEqual(str(loan), expected_str)
        self.assertAlmostEqual(
            float(loan.monthly_installment),
            float(loan.calculate_monthly_installment()),
            delta=0.01
        )

    # Test Case 3: Test Loan calculate_monthly_installment method
    def test_loan_calculate_monthly_installment(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 3',
            amount=5000,
            max_loan_amount=10000,
            min_loan_amount=200,
            interest_rate=5,
            loan_duration=12
        )
        loan = Loan.objects.create(
            customerName='Bob',
            loan_fund_ID=loan_fund,
            loan_amount=3000,
            interest_rate=5,
            duration=12,
            status='Requested'
        )

        calculated_installment = loan.calculate_monthly_installment()
        expected_installment = Decimal('262.50')

        self.assertAlmostEqual(
            float(calculated_installment),
            float(expected_installment),
            delta=0.01
        )
        self.assertEqual(str(loan.monthly_installment), str(expected_installment))

    # Test Case 4: Test loan creation with minimum loan amount
    def test_loan_creation_min_amount(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 4',
            amount=10000,
            max_loan_amount=50000,
            min_loan_amount=500,
            interest_rate=4,
            loan_duration=24
        )
        loan = Loan.objects.create(
            customerName='Charlie',
            loan_fund_ID=loan_fund,
            loan_amount=500,
            interest_rate=4,
            duration=24,
            status='Requested'
        )

        expected_str = 'Charlie - Fund 4 - 500'
        self.assertEqual(str(loan), expected_str)

    # Test Case 5: Test loan creation with maximum loan amount
    def test_loan_creation_max_amount(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 5',
            amount=30000,
            max_loan_amount=100000,
            min_loan_amount=1000,
            interest_rate=6,
            loan_duration=36
        )
        loan = Loan.objects.create(
            customerName='David',
            loan_fund_ID=loan_fund,
            loan_amount=100000,
            interest_rate=6,
            duration=36,
            status='Requested'
        )

        expected_str = 'David - Fund 5 - 100000'
        self.assertEqual(str(loan), expected_str)

    # Test Case 6: Test loan status change to 'Approved'
    def test_loan_status_approved(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 6',
            amount=2000,
            max_loan_amount=10000,
            min_loan_amount=200,
            interest_rate=3,
            loan_duration=6
        )
        loan = Loan.objects.create(
            customerName='Eve',
            loan_fund_ID=loan_fund,
            loan_amount=1000,
            interest_rate=3,
            duration=6,
            status='Approved'
        )

        expected_status = 'Approved'
        self.assertEqual(loan.status, expected_status)

    # Test Case 7: Test loan status change to 'Rejected'
    def test_loan_status_rejected(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 7',
            amount=2000,
            max_loan_amount=10000,
            min_loan_amount=200,
            interest_rate=3,
            loan_duration=6
        )
        loan = Loan.objects.create(
            customerName='Frank',
            loan_fund_ID=loan_fund,
            loan_amount=1500,
            interest_rate=3,
            duration=6,
            status='Rejected'
        )

        expected_status = 'Rejected'
        self.assertEqual(loan.status, expected_status)

    # Test Case 8: Test Check loan_amount less than min_loan_amount
    def test_loan_creation_below_min_amount(self):
        # Create a loan fund with specific attributes
        loan_fund = LoanFund.objects.create(
            name='Fund 8',
            amount=8000,
            max_loan_amount=20000,
            min_loan_amount=1000,
            interest_rate=4,
            loan_duration=12
        )
        
        # Use a context manager to check if a ValidationError is raised
        with self.assertRaises(ValidationError):
            # Try to create a Loan instance with loan_amount below min_loan_amount
            Loan.objects.create(
                customerName='Grace',
                loan_fund_ID=loan_fund,
                loan_amount=500,  # Below min_loan_amount
                interest_rate=4,
                duration=12,
                status='Requested'
            )
    # Test Case 9: Test Check loan_amount more than max_loan_amount
    def test_loan_creation_above_max_amount(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 9',
            amount=10000,
            max_loan_amount=50000,
            min_loan_amount=1000,
            interest_rate=4,
            loan_duration=12
        )
        with self.assertRaises(ValidationError):
            Loan.objects.create(
                customerName='Hannah',
                loan_fund_ID=loan_fund,
                loan_amount=60000,  # Above max_loan_amount
                interest_rate=4,
                duration=12,
                status='Requested'
            )

    # Test Case 10: Test for Invalid Interest Rate (Negative Value)
    def test_invalid_interest_rate(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 10',
            amount=10000,
            max_loan_amount=50000,
            min_loan_amount=1000,
            interest_rate=4,
            loan_duration=12
        )
        with self.assertRaises(ValidationError):
            Loan.objects.create(
                customerName='Isabella',
                loan_fund_ID=loan_fund,
                loan_amount=8000,
                interest_rate=-2,  # Negative interest rate
                duration=12,
                status='Requested'
            )

    # Test Case 11: Test cascading delete behavior between LoanFund and Loan
    def test_cascading_delete(self):
        # Create a loan fund
        loan_fund = LoanFund.objects.create(
            name='Fund 11',
            amount=10000,
            max_loan_amount=50000,
            min_loan_amount=1000,
            interest_rate=4,
            loan_duration=12
        )

        # Create loans associated with the loan fund
        loan1 = Loan.objects.create(
            customerName='John',
            loan_fund_ID=loan_fund,
            loan_amount=2000,
            interest_rate=4,
            duration=12,
            status='Requested'
        )
        loan2 = Loan.objects.create(
            customerName='Jane',
            loan_fund_ID=loan_fund,
            loan_amount=3000,
            interest_rate=4,
            duration=12,
            status='Requested'
        )

        # Ensure that loans are created
        self.assertEqual(Loan.objects.count(), 2)

        # Delete the loan fund
        loan_fund.delete()

        # Verify that associated loans are also deleted
        self.assertEqual(Loan.objects.count(), 0)


    # Test Case 12: Test handling of NULL loan_fund_ID
    def test_null_loan_fund_id(self):
        # Attempt to create a Loan instance without a loan fund
        with self.assertRaises(ValidationError):
            Loan.objects.create(
                customerName='NoLoanFund',
                loan_amount=5000,
                interest_rate=3,
                duration=6,
                status='Requested'
            )

    # Test Case 13: Test Loan Creation with Valid Status (e.g., 'Approved', 'Rejected')
    def test_loan_creation_valid_status(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 12',
            amount=10000,
            max_loan_amount=50000,
            min_loan_amount=1000,
            interest_rate=4,
            loan_duration=12
        )
        loan_approved = Loan.objects.create(
            customerName='Alice',
            loan_fund_ID=loan_fund,
            loan_amount=2000,
            interest_rate=4,
            duration=12,
            status='Approved'
        )
        loan_rejected = Loan.objects.create(
            customerName='Bob',
            loan_fund_ID=loan_fund,
            loan_amount=3000,
            interest_rate=4,
            duration=12,
            status='Rejected'
        )

        self.assertEqual(loan_approved.status, 'Approved')
        self.assertEqual(loan_rejected.status, 'Rejected')

    # Test Case 14: Test Loan Status Change to Valid Status (e.g., 'Approved', 'Rejected')
    def test_loan_status_change_valid_status(self):
        loan_fund = LoanFund.objects.create(
            name='Fund 13',
            amount=10000,
            max_loan_amount=50000,
            min_loan_amount=1000,
            interest_rate=4,
            loan_duration=12
        )
        loan = Loan.objects.create(
            customerName='Eve',
            loan_fund_ID=loan_fund,
            loan_amount=1000,
            interest_rate=4,
            duration=12,
            status='Requested'
        )

        loan.status = 'Approved'
        loan.save()
        self.assertEqual(loan.status, 'Approved')

        loan.status = 'Rejected'
        loan.save()
        self.assertEqual(loan.status, 'Rejected')

