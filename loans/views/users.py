from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from ..serializers import UserSerializer
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import logout


# List and create users
@api_view(['GET', 'POST'])
def user_list_create_view(request):
    if request.method == 'GET':
        # Retrieve all users
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create a new user
        if request.method == 'POST':
            # Extract username, password, and email from the request data
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            hashed_password = make_password(password)

            try:
                user = User.objects.create(username=username, email=email, password=hashed_password)
                
                # Add the user to the 'LoanCustomers' group
                group, created = Group.objects.get_or_create(name='LoanCustomers')
                user.groups.add(group)
                
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                error_message = str(e)  
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete user details by ID
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) 
def user_detail_view(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        # Retrieve user info by ID
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Update user info by ID
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # Delete user by ID
        user.delete()
        return Response(status=204)

# User login
@api_view(['POST'])
def user_login(request):
     # Extract username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')

    # Ensure that the user with the provided username exists
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials 1'}, status=status.HTTP_401_UNAUTHORIZED)

    if user.check_password(password):
        # User authentication successful
        token, created = Token.objects.get_or_create(user=user)  # Get or create a token
        return Response({'token': token.key, 'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
    else:
        # Invalid password
        return Response({'error': 'Invalid credentials 2'}, status=status.HTTP_401_UNAUTHORIZED)
    
