from rest_framework import serializers
from .models import Vendor, VendorOpeningHours



class VendorOpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorOpeningHours
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Vendor
        fields = '__all__'