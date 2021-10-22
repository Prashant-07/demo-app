from typing import cast
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .models import User,Roles,Activity,Operations,AccountStatus
from .forms import UserForm
from django.http import QueryDict
from .util import getRequestIp,generateToken

# Create your views here.
@csrf_exempt
def createUser(request,admin=''):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method'},status=405)

    _form = UserForm(request.POST)
    if not _form.is_valid():
        return JsonResponse({'message': _form.errors},status=400)

    name      = _form.cleaned_data['name']
    email     = _form.cleaned_data['email']
    password  = _form.cleaned_data['password']
    contact   = _form.cleaned_data['contact']
    gender    = _form.cleaned_data['gender']

    # checking if email or phone number already exisits
    existingUser =  User.objects.filter(Q(email__iexact=email) | Q(contact=contact))
    if existingUser.count():
        if existingUser[0].email == email.lower():
            return JsonResponse({'message': 'Email address already exist'},status=400)
        if existingUser[0].contact == contact:
            return JsonResponse({'message': 'Contact No. already exist'},status=400)
 
    user = User(name = name,email = email.lower(),contact = contact,role=Roles.USER,gender=gender)
    user.set_password(password)
    user.save()
    logOperation(request,Operations.LOGGEDOUT,user)
    return JsonResponse({'message': 'User account created successfully'},status=200)

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method'},status=405)
           
    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.user.is_authenticated:
        if request.user.email != username.lower() and request.user.contact != username:
            return JsonResponse({'message': 'You are logged into some other account, please remove auth token from request and try again'},status=400)
        else:
            return JsonResponse({'message': 'Already logged in'},status=200)
    
    if username and password:
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(contact=username))
            if not check_password(password,user.password):
                return JsonResponse({'message': 'Incorrect Username or Password'},status=400)
                
            if user.accountStatus == AccountStatus.INACTIVE:
               return JsonResponse({'message': 'Account is deleted by user'},status=400)
            
            if user.accountStatus == AccountStatus.BLOCKED:
               return JsonResponse({'message': 'Account is blocked by Admin'},status=400)
            
            logOperation(request,Operations.LOGGEDIN,user)
            token = generateToken(request,{'name':user.name,'email':user.email})
            user.token = token
            user.save()
            response = JsonResponse({'message': 'Logged in successfully'},status=200)
            response['HTTP_AUTHORIZATION'] = token
            return response
        
        except:
            pass
    
    else:
        return JsonResponse({'message': 'Insufficient data in request'},status=400)

def logout(request):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method'},status=405)
           
    if request.user.is_authenticated:
        user = request.user
        user.token = ''
        user.save()
        response = JsonResponse({'message': 'Logged out successfully'},status=200)
        response['HTTP_AUTHORIZATION'] = ''
        logOperation(request,Operations.LOGGEDOUT)
        return response
    else:
        JsonResponse({'message': 'Invalid request'},status=400)

@csrf_exempt
def deleteUser(request,identifier=None):
    if request.method != 'DELETE':
       return JsonResponse({'message': 'Invalid request method'},status=405)
    if not identifier and not request.user.is_authenticated:
       return JsonResponse({'message': 'Please login to perform this operation'},status=401)

    user = request.user
    user.accountStatus = AccountStatus.INACTIVE
    user.save()
    logOperation(request,Operations.DELETED)
    return JsonResponse({'message': 'User account deleted successfully'},status=200)

@csrf_exempt
def updateInfo(request):
    if request.method != 'PUT':
       return JsonResponse({'message': 'Invalid request method'},status=405)
    
    if not request.user.is_authenticated:
       return JsonResponse({'message': 'Please login to perform this operation'},status=401)
    
    data        = QueryDict(request.body)
    user        = request.user
    name        = data.get('name')
    oldpassword = data.get('oldPassword')
    newPassword = data.get('newPassword')
    
    if not name and not oldpassword and not newPassword:
        return JsonResponse({'message': 'Invalid update request'},status=400)

    if name and name != user.name:
        user.name = name

    if oldpassword and newPassword and check_password(oldpassword,user.password) and user.accountStatus == AccountStatus.ACTIVE:
        user.set_password(newPassword)
    
    user.save()
    logOperation(request,Operations.UPDATED_INFO)
    return JsonResponse({'message': 'Account information is updated successfully'},status=200)

def logOperation(request,operation,user=None):
    ip = getRequestIp(request)
    if not user and request.user.is_authenticated:
        user = request.user

    Activity.objects.create(user=user,IP = ip, operation = operation)

