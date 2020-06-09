from rest_framework import serializers
from .models import PointsDiscount, AmountDiscount, PercentDiscount
from Medias.serializers import VendorMediaSerializer


class PointsDiscountSerializer(serializers.ModelSerializer):
    image = VendorMediaSerializer(many=False, read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = PointsDiscount
        fields = '__all__'

class PointsDiscountLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsDiscount
        fields = '__all__'



class AmountDiscountSerializer(serializers.ModelSerializer):
    image = VendorMediaSerializer(many=False, read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = AmountDiscount
        fields = '__all__'

class AmountDiscountLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmountDiscount
        fields = '__all__'



class PercentDiscountSerializer(serializers.ModelSerializer):
    image = VendorMediaSerializer(many=False, read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = PercentDiscount
        fields = '__all__'

class PercentDiscountLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentDiscount
        fields = '__all__'