from django.contrib import admin

from ps_stripe.models import Customer, Product


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'client')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
