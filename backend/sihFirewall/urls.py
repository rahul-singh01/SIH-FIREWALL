from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import ApplicationListCreateAPIView, ApplicationDetailAPIView, PolicyListCreateAPIView, PolicyDetailAPIView, LogListCreateAPIView, LogDetailAPIView, AlertListCreateAPIView, AlertDetailAPIView
from . import views
# Set up routers for automatic URL routing
router = routers.DefaultRouter()

# Define URL patterns
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/applications/', ApplicationListCreateAPIView.as_view(), name='application-list-create'),
    path('api/applications/<int:pk>/', ApplicationDetailAPIView.as_view(), name='application-detail'),
    path('api/policies/', PolicyListCreateAPIView.as_view(), name='policy-list-create'),
    path('api/policies/<int:pk>/', PolicyDetailAPIView.as_view(), name='policy-detail'),
    path('api/logs/', LogListCreateAPIView.as_view(), name='log-list-create'),
    path('api/logs/<int:pk>/', LogDetailAPIView.as_view(), name='log-detail'),
    path('api/alerts/', AlertListCreateAPIView.as_view(), name='alert-list-create'),
    path('api/alerts/<int:pk>/', AlertDetailAPIView.as_view(), name='alert-detail'),
]

# Include additional URL patterns if necessary
