from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
 
    
#LOAN FUNDS MODEL 
class LoanFund(models.Model):
    name = models.CharField(max_length=100)
    #AMOUNT IS LATER FILLED BY THE LOAN PROVIDER 
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    min_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0.01)])
    loan_duration = models.IntegerField(default=12, validators=[MinValueValidator(2)]) # Duration in months

    def __str__(self):
        return self.name

#LOAN MODEL
class Loan(models.Model):
    LOAN_STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    customerName = models.CharField(max_length=100)
    loan_fund_ID = models.ForeignKey('LoanFund', on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2) #SUBTRACTED FROM LOANFUND
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2) #GIVEN FROM LOANFUND
    duration = models.IntegerField()  #GIVEN FROM LOANFUND
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='Requested')
    date_requested = models.DateField(auto_now_add=True)
    date_approved = models.DateField(null=True, blank=True)
    date_rejected = models.DateField(null=True, blank=True) 
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_monthly_installment(self):
        interest_rate_decimal = self.interest_rate / 100
        total_periods = self.duration
        monthly_payment = ((self.loan_amount * (1+interest_rate_decimal)) / total_periods)
        return round(monthly_payment, 2)
    
    def clean(self):
        if self.interest_rate <= 0:
            raise ValidationError('Interest rate must be greater than 0.')

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.monthly_installment:
            self.monthly_installment = self.calculate_monthly_installment()
        
        # Check if the loan_amount is greater than or equal to min_loan_amount
        if self.loan_amount < self.loan_fund_ID.min_loan_amount:
            raise ValidationError('Loan amount is below the minimum loan amount.')
        if self.loan_amount > self.loan_fund_ID.max_loan_amount:
            raise ValidationError('Loan amount exceeds the maximum loan amount.')
        # Check if the loan_amount is greater than or equal to min_loan_amount
        if self.loan_amount < 0:
            raise ValidationError('Loan amount cannot be negative.')
        
        
        super(Loan, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.customerName} - {self.loan_fund_ID} - {self.loan_amount}"
