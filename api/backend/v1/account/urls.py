from django.urls import path
from .views import Account

urlpatterns = [
    path('register/', Account.as_view({'post': 'register'})),
    path('info/', Account.as_view({'get': 'info_user'})),
    path('', Account.as_view({'get': 'list_user'})),
    path('change_password/', Account.as_view({'post': 'change_password'})),
    path('update_active/', Account.as_view({'post': 'update_active'})),
    path('delete/', Account.as_view({'post': 'delete_account'})),
    path('update_profile/', Account.as_view({'post': 'update_profile'}))
]
