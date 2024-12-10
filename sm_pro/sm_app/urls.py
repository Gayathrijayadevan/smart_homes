from django.urls import path
from . import views

urlpatterns=[
    path('',views.sm_login),
    path('logout',views.sm_logout),

    #------------USER------------------
    path('register',views.register),
    path('user_home',views.user_home),
    path('about',views.about),
    path('contact',views.contact),
    #------------ADMIN-----------------
    path('admin_home',views.admin_home),
    path('add_pro',views.add_products),
    path('edit_pro/<pid>',views.edit_product),
    path('del_pro/<pid>',views.delete_product),

]