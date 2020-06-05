from rest_framework import serializers
from .models import ArticleMedia, VendorMedia


class VendorMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorMedia
        fields = '__all__'


class ArticleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleMedia
        fields = '__all__'
