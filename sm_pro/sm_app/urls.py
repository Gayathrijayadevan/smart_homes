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
    path('store/<cid>',views.store),
    #------------ADMIN-----------------
    path('admin_home',views.admin_home),
    path('add_pro',views.add_products),
    path('edit_pro/<pid>',views.edit_product),
    path('del_pro/<pid>',views.delete_product),
    path('add_cate',views.add_category),
]