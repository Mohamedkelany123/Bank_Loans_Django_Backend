from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import LoanFund
from ..serializers import LoanFundSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def loanfund_list(request):
    if request.method == 'GET':
        # Retrieve all loan funds
        loanfunds = LoanFund.objects.all()
        serializer = LoanFundSerializer(loanfunds, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new loan fund
        serializer = LoanFundSerializer(data=request.data)

        if serializer.is_valid():
            # Custom validation: Check if max_loan_amount >= min_loan_amount
            max_loan_amount = serializer.validated_data.get('max_loan_amount')
            min_loan_amount = serializer.validated_data.get('min_loan_amount')

            if max_loan_amount >= min_loan_amount:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Max loan amount must be greater than or equal to min loan amount.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle other validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def loanfund_detail(request, pk):
    try:
        loanfund = LoanFund.objects.get(pk=pk)
    except LoanFund.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve loan fund details by ID
        serializer = LoanFundSerializer(loanfund)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Update loan fund amount by adding an entered amount
        serializer = LoanFundSerializer(loanfund, data=request.data, partial=True)
        if serializer.is_valid():
            
            entered_amount = request.data.get('amount', 0)
            
            if entered_amount <= 0:
                return Response({'error': 'Please enter a valid positive amount'}, status=status.HTTP_400_BAD_REQUEST)
            
            current_amount = loanfund.amount
            updated_amount = current_amount + entered_amount
    
            loanfund.amount = updated_amount
            loanfund.save()
            return Response(serializer.data)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Delete loan fund by ID
        loanfund.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
