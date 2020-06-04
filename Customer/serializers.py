from rest_framework import serializers
from .models import Customer, CustomersList


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'