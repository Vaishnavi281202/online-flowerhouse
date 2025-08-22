from django.contrib import admin

from .models import Flower, Customer, Order, Payment,PaymentType,delivery_staff,delivery
admin.site.register([Flower, Customer, Order, Payment,PaymentType,delivery_staff,delivery])