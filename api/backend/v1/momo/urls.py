from django.urls import path
from .views import Momo

urlpatterns = [
    path('pay/', Momo.as_view({'post': 'pay_with_momo'})),
]
