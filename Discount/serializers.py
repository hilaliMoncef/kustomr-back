from rest_framework import serializers
from .models import PointsDiscount, AmountDiscount, PercentDiscount


class PointsDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsDiscount
        fields = '__all__'



class AmountDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmountDiscount
        fields = '__all__'



class PercentDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentDiscount
        fields = '__all__'