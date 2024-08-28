from rest_framework import generics
from .models import Application, Policy, Log, Alert
from .serializers import ApplicationSerializer, PolicySerializer, LogSerializer, AlertSerializer

class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class PolicyListCreateView(generics.ListCreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class PolicyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class LogListView(generics.ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

class AlertListView(generics.ListAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
