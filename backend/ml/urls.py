from django.urls import path
from . import views

app_name = 'ml'

urlpatterns = [
    path('train/', views.TrainModelView.as_view(), name='train_model'),
    path('predict/', views.PredictView.as_view(), name='predict'),
    path('metrics/', views.MetricsView.as_view(), name='metrics'),
]
