from django.test import TestCase
from .models import Drink, LoanFund, Loan

class DrinkModelTest(TestCase):
    def test_drink_str_representation(self):
        drink = Drink(name="Coffee", description="Delicious coffee")
        self.assertEqual(str(drink), "Coffee Delicious coffee")

class LoanFundModelTest(TestCase):
    def test_loan_fund_str_representation(self):
        fund = LoanFund(name="Emergency Fund", amount=1000, max_loan_amount=5000, min_loan_amount=100, interest_rate=5.0, loan_duration=12)
        self.assertEqual(str(fund), "Emergency Fund")

class LoanModelTest(TestCase):
    def test_calculate_monthly_installment(self):
        fund = LoanFund.objects.create(name="Test Fund", amount=10000, max_loan_amount=10000, min_loan_amount=1000, interest_rate=5.0, loan_duration=12)
        loan = Loan(customerName="John Doe", loan_fund_ID=fund, loan_amount=5000, interest_rate=5.0, duration=12)
        expected_monthly_payment = 439.77  # Calculated based on formula and values above
        self.assertAlmostEqual(loan.calculate_monthly_installment(), expected_monthly_payment, places=2)

    def test_monthly_installment_saved_on_create(self):
        fund = LoanFund.objects.create(name="Another Fund", amount=10000, max_loan_amount=10000, min_loan_amount=1000, interest_rate=5.0, loan_duration=12)
        loan = Loan.objects.create(customerName="Jane Smith", loan_fund_ID=fund, loan_amount=2000, interest_rate=5.0, duration=12)
        expected_monthly_payment = 183.95  # Calculated based on formula and values above
        self.assertEqual(loan.monthly_installment, expected_monthly_payment)

    # You can add more tests for different scenarios, such as status changes, etc.
