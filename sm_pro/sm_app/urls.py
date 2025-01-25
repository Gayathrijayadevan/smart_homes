from django.urls import path
from . import views
 
urlpatterns=[
    path('',views.user_home),           #for user dashboard

    path('login',views.sm_login),       #for login

    path('logout',views.sm_logout),     # for logout

    path('register',views.register),    #for user registration

    path('admin_home',views.admin_home),# for admin dashboard


    #------------USER------------------
    path('about',views.about),                  #for user aboutpage

    path('contact',views.contact),              #for user contact page

    path('store',views.store,name='store'),     #for user store page

    path('pro_dtl/<int:pid>', views.view_pro_dtls, name='view_pro_dtls'),  # for user to view specific product details

    path('cart',views.cart),                    #for user to view cart

    path('add_to_cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),  #for adding products to cart

    path('qty_in/<cid>',views.qty_in),          #to increase the  product quantity

    path('qty_dec/<cid>',views.qty_dec),        #to decrease the  product quantity

    path('remove/<cid>',views.remove_pro),      # to remove the product from cart

    path('booking',views.bookings),             #for user to see all the bookings made

    path('order/<pid>',views.order),            #to collect order details

    path('pay/<pid>', views.payment, name='pay'), # to collect payment details

    path('pro_buy/', views.pro_buy, name='pro_buy'), #to add pro to buy

    path('order_remv/<oid>',views.remove_order),     #to remove ordered product

    path('visit',views.visit),                       #to schdeul visit

    path("payment/", views.payment, name="payment"),  #for online payment gateway
    path("razorpay/callback/", views.callback, name="callback"),



    #------------ADMIN-----------------


    path('add_pro',views.add_products),        #to add products

    path('edit_pro/<pid>',views.edit_product), #to edit product details

    path('del_pro/<pid>',views.delete_product),#to delete the product

    path('add_cate',views.add_category),       #to add  product category

    path('ad_view_pro',views.ad_viewp),        #to view all product 

    path('ad_pro_dtls/<pid>',views.ad_pro_dtls),#to view specific product details

    path('enquires',views.enquire),             #to view all user enquires

    path('u_bookings',views.view_bookings),      #to view all user bookings

    path('view_users',views.view_users),         #to see all users
    
    path('view visit',views.view_vists),         #to see all user  schedule visits
]