# dashboard/urls.py
from django.urls import path
from .views import dashboard_view, summary_view, data_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('summary/', summary_view, name='summary'),
    path('data/', data_view, name='data'),
]

