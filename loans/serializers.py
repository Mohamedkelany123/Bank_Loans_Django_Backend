#Describes object going from python to json object
from rest_framework import serializers 
from django.contrib.auth.models import User
from .models import  LoanFund, Loan


class LoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFund
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Loan
        fields = '__all__'