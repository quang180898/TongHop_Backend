from django.urls import path
from api.backend.v1.customer_shoes.views import AccountShoes

urlpatterns = [
    path('', AccountShoes.as_view({'get': 'list_shoes_account'})),
    path('history/', AccountShoes.as_view({'get': 'history'})),
    path('detail/', AccountShoes.as_view({'get': 'detail_shoes_account'})),
    path('most_buy/', AccountShoes.as_view({'get': 'most_buy'})),
    path('create/', AccountShoes.as_view({'post': 'create'})),
    path('update/', AccountShoes.as_view({'post': 'update_shoes_account'})),
    path('delete/', AccountShoes.as_view({'post': 'delete_shoes_account'})),
]
