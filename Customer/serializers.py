from rest_framework import serializers
from .models import Customer, CustomersList, Transaction
from Vendor.serializers import VendorSerializer


class CustomerSerializer(serializers.ModelSerializer):
    visit_freq = serializers.ReadOnlyField()
    last_visit = serializers.ReadOnlyField()
    total_expenses = serializers.ReadOnlyField()
    avg_expenses = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = '__all__'

class CustomerFullSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False, read_only=True)
    visit_freq = serializers.ReadOnlyField()
    last_visit = serializers.ReadOnlyField()
    total_expenses = serializers.ReadOnlyField()
    avg_expenses = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersList
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'