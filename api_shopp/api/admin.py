from django.contrib import admin

# Register your models here.
from .models import Product, Orders,OrderUpdate,Seller,Customer


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','update_desc']

admin.site.register(OrderUpdate,OrderAdmin)

admin.site.register(Product)

admin.site.register(Orders)

admin.site.register(Seller)
admin.site.register(Customer)