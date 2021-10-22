from django.urls import path
from .views import *

urlpatterns = [
    path('createAdminAccount',createAdmin),
    path('getUserActivities/<str:identifier>',getUserActivity),
    path('getAllUsersActivities',getAllUsersActivities),
    path('blockUser/<str:identifier>',blockUser),
    path('unblockUser/<str:identifier>',unblockUser)
]