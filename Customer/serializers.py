from rest_framework import serializers
from .models import Customer, CustomersList
from Vendor.serializers import VendorSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerFullSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False, read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'