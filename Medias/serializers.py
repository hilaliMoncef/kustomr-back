from rest_framework import serializers
from .models import ArticleMedia, VendorMedia, DiscountMedia, TrainingMedia, EmailMedia


class VendorMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorMedia
        fields = '__all__'


class ArticleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleMedia
        fields = '__all__'


class DiscountMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountMedia
        fields = '__all__'


class TrainingMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingMedia
        fields = '__all__'


class EmailMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMedia
        fields = '__all__'
