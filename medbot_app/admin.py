from django.contrib import admin

# Register your models here.

from .models import Admin, Customer, Employee, Coupon, Delivery, Inventory, Cart, Order, Prescription, OrderedCart

admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Coupon)
admin.site.register(Delivery)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(Prescription)
admin.site.register(Cart)
admin.site.register(OrderedCart)