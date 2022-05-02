from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('backend/', include('api.backend.urls'))
]
