from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import Training
from .serializers import TrainingLightSerializer, TrainingSerializer

class ListTrainings(generics.ListAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Training.objects.order_by('-date_added')
        else:
            return Training.objects.filter(is_active=True).order_by('-date_added')


class CreateTrainings(generics.CreateAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingLightSerializer
    permission_classes = [permissions.IsAdminUser]


class RetrieveUpdateDestroyTrainings(generics.RetrieveUpdateDestroyAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return TrainingLightSerializer
        return TrainingSerializer