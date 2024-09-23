from django.urls import path 
from . import views
urlpatterns =[
    path('register-user/', views.registerUser, name='registerUser' ),
    path('register-vendor/', views.registerVendor, name='registerVendor' ),
    path('login/', views.login, name='login' ),
    path('logout/', views.logout, name='logout' ),
    path('customerDasboard/', views.custDashboard, name='customerDasboard' ),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard' ),
    path('myAccount/', views.myAccount, name='myAccount' ),
    path('activate/<uidb64>/<token>/', views.activate, name='activate' ),
]