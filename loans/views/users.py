from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth.models import User
from ..serializers import UserSerializer
from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Hash the password using set_password
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete user details by ID
@api_view(['GET', 'PUT', 'DELETE'])
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
    
    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user:
        return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
