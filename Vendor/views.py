from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from .models import Vendor, RewardCardLayout, VendorOpeningHours
from .serializers import VendorSerializer, RewardCardLayoutSerializer, RewardCardLayoutLightSerializer, VendorOpeningHoursSerializer
from Customer.models import Customer, CustomersList, Transaction
from Customer.serializers import CustomerSerializer, CustomerListSerializer


class CurrentVendor(APIView):
    """
    View to get the current user's info
    """

    def get(self, request, format=None):
        if request.user.is_authenticated and request.user.is_vendor:
            return Response(VendorSerializer(request.user.vendor).data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Aucun utilisateur connecté.'}, status=status.HTTP_403_FORBIDDEN)


class UpdateVendor(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateHourVendor(generics.UpdateAPIView):
    queryset = VendorOpeningHours.objects.all()
    serializer_class = VendorOpeningHoursSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateLayoutVendor(generics.UpdateAPIView):
    queryset = RewardCardLayout.objects.all()
    serializer_class = RewardCardLayoutLightSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListCreateCustomers(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Customer.objects.order_by('-pk')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return Customer.objects.filter(vendor=user.vendor).order_by('-pk')
            else:
                return Customer.objects.none()


class ListCreateCustomersList(generics.ListCreateAPIView):
    queryset = CustomersList.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomersList.objects.order_by('-last_update')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return CustomersList.objects.filter(vendor=user.vendor).order_by('-last_update')
            else:
                return CustomersList.objects.none()