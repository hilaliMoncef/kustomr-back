from rest_framework import serializers
from .models import Vendor, VendorOpeningHours, RewardCardLayout, Article
from Medias.serializers import ArticleMediaSerializer, VendorMediaSerializer


class RewardCardLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardCardLayout
        fields = '__all__'


class VendorOpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorOpeningHours
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Vendor
        fields = '__all__'


class VendorFullSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    reward_card_layout = RewardCardLayoutSerializer(many=False, read_only=True)
    opening_hours = VendorOpeningHoursSerializer(many=False, read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'



class ArticlesSerializer(serializers.ModelSerializer):
    image = ArticleMediaSerializer(many=False, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'