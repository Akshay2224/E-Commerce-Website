from rest_framework import serializers

from .models import Product,Orders,Customer

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name','category','subcategory','price','desc','pub_date','image','seller_name','qty')
class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ('name','email','address','city','state','zip_code','phone')
class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Customer
        fields = ('username','email','password','first_name','last_name','phone_number')