from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import PointsDiscount, AmountDiscount, PercentDiscount
from .serializers import PointsDiscountSerializer, AmountDiscountSerializer, PercentDiscountSerializer, PointsDiscountLightSerializer, AmountDiscountLightSerializer, PercentDiscountLightSerializer


class ListDiscounts(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        data = {}
        if user.is_authenticated:
            if user.is_vendor:
                data['points'] = PointsDiscountSerializer(PointsDiscount.objects.filter(vendor=user.vendor).order_by('-last_update'), many=True).data
                data['amount'] = AmountDiscountSerializer(AmountDiscount.objects.filter(vendor=user.vendor).order_by('-last_update'), many=True).data
                data['percent'] = PercentDiscountSerializer(PercentDiscount.objects.filter(vendor=user.vendor).order_by('-last_update'), many=True).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Méthode uniquement reservée aux commerçants'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListCreatePointsDiscounts(generics.ListCreateAPIView):
    queryset = PointsDiscount.objects.all()
    serializer_class = PointsDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PointsDiscount.objects.order_by('-last_update')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return PointsDiscount.objects.filter(vendor=user.vendor).order_by('-last_update')
            else:
                return PointsDiscount.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PointsDiscountLightSerializer
        return PointsDiscountSerializer

class RetrieveUpdateDestroyPointsDiscounts(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointsDiscount.objects.all()
    serializer_class = PointsDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PointsDiscountLightSerializer
        return PointsDiscountSerializer


class ListCreateAmountDiscounts(generics.ListCreateAPIView):
    queryset = AmountDiscount.objects.all()
    serializer_class = AmountDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AmountDiscount.objects.order_by('-last_update')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return AmountDiscount.objects.filter(vendor=user.vendor).order_by('-last_update')
            else:
                return AmountDiscount.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return AmountDiscountLightSerializer
        return AmountDiscountSerializer

class RetrieveUpdateDestroyAmountDiscounts(generics.RetrieveUpdateDestroyAPIView):
    queryset = AmountDiscount.objects.all()
    serializer_class = AmountDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return AmountDiscountLightSerializer
        return AmountDiscountSerializer


class ListCreatePercentDiscounts(generics.ListCreateAPIView):
    queryset = PercentDiscount.objects.all()
    serializer_class = PercentDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PercentDiscount.objects.order_by('-last_update')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return PercentDiscount.objects.filter(vendor=user.vendor).order_by('-last_update')
            else:
                return PercentDiscount.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PercentDiscountLightSerializer
        return PercentDiscountSerializer

class RetrieveUpdateDestroyPercentDiscounts(generics.RetrieveUpdateDestroyAPIView):
    queryset = PercentDiscount.objects.all()
    serializer_class = PercentDiscountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PercentDiscountLightSerializer
        return PercentDiscountSerializer