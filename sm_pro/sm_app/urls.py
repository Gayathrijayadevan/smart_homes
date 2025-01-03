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
    path('store',views.store,name='store'),
    path('pro_dtl/<pid>',views.view_pro_dtls),
    path('cart',views.cart),
    path('add_to_cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('remove/<cid>',views.remove_pro),
    path('booking',views.bookings),
    path('cart_buy/<cid>',views.cart_buy),
    path('order/<pid>',views.order),
    path('pay/<pid>', views.payment, name='pay'),
    path('pro_buy/', views.pro_buy, name='pro_buy'),
    path('order_remv/<oid>',views.remove_order),

    #------------ADMIN-----------------
    path('admin_home',views.admin_home),
    path('add_pro',views.add_products),
    path('edit_pro/<pid>',views.edit_product),
    path('del_pro/<pid>',views.delete_product),
    path('add_cate',views.add_category),
    path('ad_view_pro',views.ad_viewp),
    path('ad_pro_dtls/<pid>',views.ad_pro_dtls),
    path('enquires',views.enquire),
    path('u_bookings',views.view_bookings),
]