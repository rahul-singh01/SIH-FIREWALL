from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('policies/', views.PolicyListView.as_view(), name='policy_list'),
    path('policies/<int:pk>/', views.PolicyDetailView.as_view(), name='policy_detail'),
    path('logs/', views.LogListView.as_view(), name='log_list'),
    path('alerts/', views.AlertListView.as_view(), name='alert_list'),
]
