from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Application, Policy, Log, Alert
from .serializers import ApplicationSerializer, PolicySerializer, LogSerializer, AlertSerializer
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.shortcuts import render
import json

# # Serve React App
# index = never_cache(TemplateView.as_view(template_name='index.html'))

def index(request):
    if settings.DEBUG:
        return render(request, 'index.html', {'debug': True})
    else:
        manifest_path = settings.STATIC_ROOT / 'dist' / 'manifest.json'
        with open(manifest_path, 'r') as manifest_file:
            manifest = json.load(manifest_file)
        return render(request, 'index.html', {'debug': False, 'manifest': manifest})
class ApplicationListCreateAPIView(APIView):
    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return None

    def get(self, request, pk):
        application = self.get_object(pk)
        if application is None:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        application = self.get_object(pk)
        if application is None:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        application = self.get_object(pk)
        if application is None:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Similar views for Policy, Log, and Alert can be created using the pattern above.

# Example for Policy:
class PolicyListCreateAPIView(APIView):
    def get(self, request):
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PolicyDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Policy.objects.get(pk=pk)
        except Policy.DoesNotExist:
            return None

    def get(self, request, pk):
        policy = self.get_object(pk)
        if policy is None:
            return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PolicySerializer(policy)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        policy = self.get_object(pk)
        if policy is None:
            return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        policy = self.get_object(pk)
        if policy is None:
            return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)
        policy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
