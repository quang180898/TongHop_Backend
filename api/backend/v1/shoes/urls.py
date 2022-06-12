from django.urls import path

from api.backend.v1.shoes.views import ShoesStore

urlpatterns = [
    path('', ShoesStore.as_view({'get': 'list_shoes'})),
    path('home/', ShoesStore.as_view({'get': 'list_home'})),
    path('detail/', ShoesStore.as_view({'get': 'detail_shoes'})),
    path('same_category/', ShoesStore.as_view({'get': 'shoes_same_category'})),
    path('delete/', ShoesStore.as_view({'post': 'delete_shoes'})),
    path('create_or_update/', ShoesStore.as_view({'post': 'create_or_update'}))
]
