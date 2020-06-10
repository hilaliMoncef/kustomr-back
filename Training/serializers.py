from rest_framework import serializers
from .models import Training
from Medias.serializers import TrainingMediaSerializer


class TrainingSerializer(serializers.ModelSerializer):
    poster = TrainingMediaSerializer(many=False, read_only=True)
    
    class Meta:
        model = Training
        fields = '__all__'


class TrainingLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'