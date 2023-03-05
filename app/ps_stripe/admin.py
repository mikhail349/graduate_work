from django.contrib import admin

from ps_stripe.models import Customer, Product

admin.site.register(Customer)
admin.site.register(Product)
