from django.urls import path
from .views import (
    ApplicationListCreateView,
    ApplicationRetrieveUpdateDestroyView,
    PolicyListCreateView,
    PolicyRetrieveUpdateDestroyView,
    LogListView,
    AlertListView,
)

urlpatterns = [
    path('applications/', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationRetrieveUpdateDestroyView.as_view(), name='application-retrieve-update-destroy'),
    path('policies/', PolicyListCreateView.as_view(), name='policy-list-create'),
    path('policies/<int:pk>/', PolicyRetrieveUpdateDestroyView.as_view(), name='policy-retrieve-update-destroy'),
    path('logs/', LogListView.as_view(), name='log-list'),
    path('alerts/', AlertListView.as_view(), name='alert-list'),
]
