from django.db import models

class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ' ' + self.description 
    
class LoanFund(models.Model):
    name = models.CharField(max_length=100)
    #This field stores the total budget or amount available in the loan fund
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    loan_duration = models.IntegerField(default=12) # Duration in months

    def __str__(self):
        return self.name
