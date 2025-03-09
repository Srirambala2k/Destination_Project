from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Account, Destination, Log, Role, AccountMember
from django.contrib.auth import authenticate, login 
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt ## not good for production
import json
from .tasks import send_data_to_destination
from .validators import validate_email, validate_website
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer,DestinationSerializer,AccountMemberSerializer,LogSerializer,RoleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


## validating the email
def is_valid_email(email):
    try:
        validator = EmailValidator()
        validator(email)
    except ValidationError:
        return False
    return True

## validating the domain
def valid_email_domain(email, allowed_domains=None):
    if allowed_domains:
        domain = email.split('@')[1]
        if domain not in allowed_domains:
            return False
    return True


## @csrf_exempt ---> dont use for production only for testing purpose
## Register or create a new user
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            data = json.loads(request.body.decode('utf-8'))  # Parse JSON request data

            username = data.get('username')  
            password = data.get('password') 
            email = data.get('email')  

            if not username or not password or not email:
                return JsonResponse({"error": "All fields are required."}, status=400)

            allowed_domains = ['gmail.com']
            if not valid_email_domain(email, allowed_domains):
                return JsonResponse({"error": f"Email domain must be one of {allowed_domains}."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists."}, status=400)

            # Create a user
            user = User.objects.create_user(username=email, email=email, password=password)

            # Authenticate and log in the user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Registration successful."}, status=201)
            else:
                return JsonResponse({"error": "Authentication failed."}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    return JsonResponse({"error": "Only POST method is allowed."}, status=405)

       
## login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('Password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request,user)
            return JsonResponse({'message': 'successfully loged in'})
        else:
            return JsonResponse({"error":"invalid username or password"}, status=400)
    return Json({"error":"only post method is allowed"}, status=400)


##Log out view
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "Logged out successfully."})
    else:
        return JsonResponse({"error": "User not logged in."}, status=400)



##Trigger the Celery Task
def data_handler(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        destination_id = data.get('destination_id')

        # Asynchronously send data to destination
        send_data_to_destination.delay(data, destination_id)

        return JsonResponse({"message": "Data received and being processed"}, status=202)


def create_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Validate the email for the User model
            validate_email_field(data['email'])
            
            # Validate the website for the Account model
            validate_website_field(data['website'])
            
           
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password']
            )
            
            # Create Account instance
            account = Account.objects.create(
                user=user,  
                website=data['website'],
                
            )
            
            return JsonResponse({"message": "Account created successfully."}, status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]


class AccountMemberViewSet(viewsets.ModelViewSet):
    queryset = AccountMember.objects.all()
    serializer_class = AccountMemberSerializer
    permission_classes = [IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

