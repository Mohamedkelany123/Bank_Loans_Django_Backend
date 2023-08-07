from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import LoanFund
from ..serializers import LoanFundSerializer

@api_view(['GET', 'POST'])
def loanfund_list(request):
    if request.method == 'GET':
        loanfunds = LoanFund.objects.all()
        serializer = LoanFundSerializer(loanfunds, many=True)
        return Response(serializer.data)

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

    if request.method == 'GET':
        serializer = LoanFundSerializer(loanfund)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LoanFundSerializer(loanfund, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        loanfund.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
