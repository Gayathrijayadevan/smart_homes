from django.urls import path
from . import views

urlpatterns=[
    path('',views.sm_login),
    path('logout',views.sm_logout),
    path('register',views.register),
    path('user_home',views.user_home),
]