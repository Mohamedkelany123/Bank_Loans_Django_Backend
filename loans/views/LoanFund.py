from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import LoanFund
from ..serializers import LoanFundSerializer


@api_view(['GET', 'POST'])
def loanfund_list(request):
    #GET ALL LOAN FUNDS
    if request.method == 'GET':
        loanfunds = LoanFund.objects.all()
        serializer = LoanFundSerializer(loanfunds, many=True)
        return Response(serializer.data)

    #CREATE A LOAN FUND
    elif request.method == 'POST':
        serializer = LoanFundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def loanfund_detail(request, pk):
    try:
        loanfund = LoanFund.objects.get(pk=pk)
    except LoanFund.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #GET LOAN FUND BY ID
    if request.method == 'GET':
        serializer = LoanFundSerializer(loanfund)
        return Response(serializer.data)

    #ACCUMLATE THE AMOUNT
    if request.method == 'PUT':
        serializer = LoanFundSerializer(loanfund, data=request.data, partial=True)
        if serializer.is_valid():
            entered_amount = request.data.get('amount', 0)
            current_amount = loanfund.amount
            updated_amount = current_amount + entered_amount

            if loanfund.min_loan_amount <= updated_amount <= loanfund.max_loan_amount:
                loanfund.amount = updated_amount
                loanfund.save()
                return Response(serializer.data)
            else:
                return Response({'error': 'The updated amount is not within the allowed range.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #DELETE LOAN FUND BY ID
    elif request.method == 'DELETE':
        loanfund.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


