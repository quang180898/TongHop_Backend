from django.urls import path

from api.backend.v1.discount.views import ShoesDiscount

urlpatterns = [
    path('', ShoesDiscount.as_view({'get': 'list_discount'})),
    path('detail/', ShoesDiscount.as_view({'get': 'detail_discount'})),
    path('create_or_update/', ShoesDiscount.as_view({'post': 'create_or_update'})),
    path('delete/', ShoesDiscount.as_view({'post': 'delete_discount'})),
]
