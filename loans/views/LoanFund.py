from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import LoanFund
from ..serializers import LoanFundSerializer

@api_view(['GET', 'POST'])
def loanfund_list(request):
    if request.method == 'GET':
        # Retrieve all loan funds
        loanfunds = LoanFund.objects.all()
        serializer = LoanFundSerializer(loanfunds, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new loan fund
        serializer = LoanFundSerializer(data=request.data)

        # Additional validation for numeric fields
        if not serializer.is_valid():
            error_messages = {}
            for field, errors in serializer.errors.items():
                if field in ['amount', 'max_loan_amount', 'min_loan_amount', 'interest_rate', 'loan_duration']:
                    error_messages[field] = 'Invalid value for numeric field.'

            return Response({"error" : error_messages}, status=status.HTTP_400_BAD_REQUEST)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle validation errors with custom messages
            error_messages = {}
            for field, errors in serializer.errors.items():
                if field == 'amount':
                    error_messages[field] = 'The updated amount is not within the allowed range.'
                elif field == 'max_loan_amount':
                    error_messages[field] = 'The max loan amount must be greater than or equal to 0.'
                elif field == 'min_loan_amount':
                    error_messages[field] = 'The min loan amount must be greater than or equal to 0.'
                elif field == 'interest_rate':
                    error_messages[field] = 'The interest rate must be greater than or equal to 0.01.'
                elif field == 'loan_duration':
                    error_messages[field] = 'The loan duration must be greater than or equal to 2.'
                else:
                    error_messages[field] = errors

            return Response({"error" : error_messages}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
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
            current_amount = loanfund.amount
            updated_amount = current_amount + entered_amount

            if loanfund.min_loan_amount <= updated_amount:
                loanfund.amount = updated_amount
                loanfund.save()
                return Response(serializer.data)
            else:
                return Response({'error': 'The updated amount is not within the allowed range.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Delete loan fund by ID
        loanfund.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
