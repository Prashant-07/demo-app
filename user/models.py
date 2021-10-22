from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.deletion import CASCADE

# Create your models here.
class Gender:
    MALE,FEMALE,OTHER = 1,2,3
    GENDER = (
        (MALE,'MALE'),
        (FEMALE,'FEMALE'),
        (OTHER,'OTHER')
    )

class Roles:
    ADMIN,USER = 1,2
    ROLES = (
        (ADMIN,'ADMIN'),
        (USER,'USER'),
    )

class Operations:
    LOGGEDIN,LOGGEDOUT = 1,2
    UPDATED_INFO,DELETED,CREATED = 3,4,5

    OPERATIONS = (
        (LOGGEDIN,'Logged in'),
        (LOGGEDOUT,'Logged out'),
        (UPDATED_INFO,'Updated Account Info'),
        (DELETED,'Deleted account'),
        (CREATED,'Created a new account')
    )

class AccountStatus:
    ACTIVE,INACTIVE,BLOCKED = 1,2,3

    STATUS = (
        (ACTIVE,'Active'),
        (INACTIVE,'Inactive'),
        (BLOCKED,'Blocked'),
    )

class User(AbstractBaseUser):
    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    contact = models.CharField(max_length=13)
    gender  = models.IntegerField(choices=Gender.GENDER)
    role    = models.IntegerField(choices=Roles.ROLES)
    accountStatus  = models.IntegerField(choices=AccountStatus.STATUS,default=AccountStatus.ACTIVE)
    token   = models.CharField(max_length=500,null=True,blank=True,default='')
    USERNAME_FIELD = 'email'

class Activity(models.Model):
    user      = models.ForeignKey(User,on_delete=CASCADE)
    operation = models.IntegerField(choices=Operations.OPERATIONS)
    IP = models.CharField(max_length=36,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)    