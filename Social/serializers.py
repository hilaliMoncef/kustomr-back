from rest_framework import serializers
from .models import FacebookPost
from Medias.serializers import SocialMediaSerializer


class FacebookPostSerializer(serializers.ModelSerializer):
    media = SocialMediaSerializer(many=False, read_only=True)

    class Meta:
        model = FacebookPost
        fields = '__all__'

class FacebookPostSerializerLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPost
        fields = '__all__'