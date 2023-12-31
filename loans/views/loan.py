from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Loan, LoanFund
from ..serializers import LoanSerializer
import datetime
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def loan_list_create_view(request):
    if request.method == 'GET':
        # Retrieve all loans
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new loan
        loan_fund_id = request.data.get('loan_fund_id', None)
        amount = request.data.get('amount', 0)

        #Make sure loanFund ID is given
        if not loan_fund_id:
            return Response({'error': 'loan_fund_id must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Make sure loanFund ID is available 
        try:
            loan_fund = LoanFund.objects.get(pk=loan_fund_id)
        except LoanFund.DoesNotExist:
            return Response({'error': 'LoanFund with the provided id does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        loan_amount = Decimal(amount)
        loan_fund_amount = Decimal(loan_fund.amount)

        #Make sure loan amound is within the range
        if loan_fund_amount < loan_amount:
            return Response({'error': 'Amount Exceeds Funds'}, status=status.HTTP_400_BAD_REQUEST)
        elif loan_fund.min_loan_amount > loan_amount:
            return Response({'error': 'Amount less than Min Loan Amount'}, status=status.HTTP_400_BAD_REQUEST)

        loan_data = {
            'customerName': request.data.get('customerName', None),
            'loan_fund_ID': loan_fund_id,
            'loan_amount': amount,
            'interest_rate': loan_fund.interest_rate,
            'duration': loan_fund.loan_duration,
            'status': request.data.get('status', 'Requested'),
        }

        serializer = LoanSerializer(data=loan_data)
        if serializer.is_valid():
            serializer.save()

            # Update the amount in the LoanFund object
            loan_fund.amount -= loan_amount
            loan_fund.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def approve_loan(request, loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan with the provided id does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    #Approve the loan
    loan.status = 'Approved'
    loan.date_approved = datetime.date.today()
    loan.save()

    return Response({'message': 'Loan approved successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_loan(request, loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan with the provided id does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    # Reject the loan
    loan.status = 'Rejected'
    loan.date_rejected = datetime.date.today()
    loan.save()

    return Response({'message': 'Loan rejected successfully.'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteLoan(request, loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan with the provided id does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete the loan
    loan.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_loans_by_username(request, username):

    loans = Loan.objects.filter(customerName=username)

    # Check if loans for the given username exist
    if not loans:
        return Response({'error': 'No loans found for the provided username.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)
