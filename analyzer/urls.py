from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('configure/', views.configure_model, name='configure'),
    path('retrain/', views.retrain_model, name='retrain'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('classification/', views.classification_view, name='classification'),
    path('regression/', views.regression_view, name='regression'),
    path('dataset/', views.dataset_view, name='dataset'),
    path('api/metrics/', views.api_metrics, name='api_metrics'),
]

