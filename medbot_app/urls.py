from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('login', views.loginC, name='loginC'),
    path('User', views.loginCustomer, name='loginCustomer'),
    path('logout', views.logoutC, name='logoutC'),
    path('register', views.registerC, name='registerC'),
    path('myaccount', views.settingsC, name='settingsC'),
    path('Admin-Page', views.loginA, name='adminpage'),
    path('Pharmacy', views.loginE, name='pharmacypage'),
    path('added/<list_id>', views.add_cart, name='add'),
    path('Cart', views.cart, name= 'cart'),
    path('user', views.customerPortal, name='customerx'),
    path('Checkout', views.checkoutOrder, name='checkoutC'),
    path('Add-item', views.addItemA, name='addItemA'),
    path('Order-History', views.orderHistoryE, name='orderHistoryE'),
    path('Order', views.orderC, name= 'orderC'),
    path('Order-History', views.orderHistoryC, name='orderHistoryC'),
]
