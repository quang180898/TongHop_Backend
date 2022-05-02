from django.urls import path

from api.backend.v1.category.views import ShoesCategory

urlpatterns = [
    path('', ShoesCategory.as_view({'get': 'list_category'})),
    path('detail/', ShoesCategory.as_view({'get': 'detail_category'})),
    path('create_or_update/', ShoesCategory.as_view({'post': 'create_or_update'})),
    path('delete/', ShoesCategory.as_view({'post': 'delete_category'})),
]
