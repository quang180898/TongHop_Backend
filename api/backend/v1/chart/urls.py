from django.urls import path
from api.backend.v1.chart.views import Chart

urlpatterns = [
    path('all/', Chart.as_view({'get': 'all'})),
    path('total/', Chart.as_view({'get': 'total'})),
]
