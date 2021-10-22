from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from user.models import User,Activity,Roles,AccountStatus
from .util import serializeActivity
from user.forms import UserForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def createAdmin(request):
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
 
    user = User(name = name,email = email.lower(),contact = contact,role=Roles.ADMIN,gender=gender)
    user.set_password(password)
    user.save()
    return JsonResponse({'message': 'Admin account created successfully'},status=200)

def getUserActivity(request,identifier=''):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method'},status=405)
    
    if not request.user.is_authenticated or request.user.role != Roles.ADMIN:
        return JsonResponse({'message': "Current role doesn't have permission for this operation"},status=403)

    try:
        if identifier.isnumeric():
            user = User.objects.get(Q(email__iexact=identifier) | Q(contact=identifier) | Q(id=identifier))
        else:
            user = User.objects.get(Q(email__iexact=identifier) | Q(contact=identifier))
                
    except:
        return JsonResponse({'message': 'No user found with this identifier'},status=400)

    activities = Activity.objects.select_related('user').filter(user_id=user.id).order_by('-timestamp')
    if not activities:
        return JsonResponse({'data': {}},status=200)

    serializedActivities = serializeActivity(activities)
    return JsonResponse(serializedActivities,status=200)

def getAllUsersActivities(request):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method'},status=405)
    
    if not request.user.is_authenticated or request.user.role != Roles.ADMIN:
        return JsonResponse({'message': "Current role doesn't have permission for this operation"},status=403)

    activities = Activity.objects.select_related('user').all().order_by('-timestamp')
    if not activities:
        return JsonResponse({'data': {}},status=200)

    serializedActivities = serializeActivity(activities)
    return JsonResponse(serializedActivities,status=200)
    
@csrf_exempt
def blockUser(request,identifier):
    if request.method != 'PUT':
        return JsonResponse({'message': 'Invalid request method'},status=405)
    
    if not request.user.is_authenticated or request.user.role != Roles.ADMIN:
        return JsonResponse({'message': "Current role doesn't have permission for this operation"},status=403)

    try:

        if identifier.isnumeric():
            user = User.objects.get(Q(email__iexact=identifier) | Q(contact=identifier) | Q(id=identifier))
        else:
            user = User.objects.get(Q(email__iexact=identifier) | Q(contact=identifier))

        if user.id == request.user.id:
            return JsonResponse({'message': 'You cannot block own account'},status=400)
        
        if user.accountStatus == AccountStatus.BLOCKED:
            return JsonResponse({'message': 'Account is already blocked'},status=200)
            
    except:
        return JsonResponse({'message': 'No user found with this identifier'},status=400)

    user.accountStatus = AccountStatus.BLOCKED
    user.save()
    return JsonResponse({'message': 'User account blocked successfully'},status=200)


@csrf_exempt
def unblockUser(request,identifier):
    if request.method != 'PUT':
        return JsonResponse({'message': 'Invalid request method'},status=405)
    
    if not request.user.is_authenticated or request.user.role != Roles.ADMIN:
        return JsonResponse({'message': "Current role doesn't have permission for this operation"},status=403)

    try:
        if identifier.isnumeric():
            user = User.objects.get(Q(email__iexact=identifier) | Q(contact=identifier) | Q(id=identifier))
        else:
            user = User.objects.get(Q(email__iexact=identifier) | Q(contact=identifier))
        
        if user.accountStatus == AccountStatus.ACTIVE:
            return JsonResponse({'message': 'Account is already unblocked'},status=200)
                        
    except:
        return JsonResponse({'message': 'No user found with this identifier'},status=400)

    user.accountStatus = AccountStatus.ACTIVE
    user.save()
    return JsonResponse({'message': 'User account unblocked successfully'},status=200)
