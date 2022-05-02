from django.urls import path

from api.backend.v1.brand.views import ShoesBrand

urlpatterns = [
    path('', ShoesBrand.as_view({'get': 'list_brand'})),
    path('detail/', ShoesBrand.as_view({'get': 'detail_brand'})),
    path('create_or_update/', ShoesBrand.as_view({'post': 'create_or_update'})),
    path('delete/', ShoesBrand.as_view({'post': 'delete_brand'})),
]
