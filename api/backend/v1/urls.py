from django.conf.urls import include
from django.urls import path

from api.backend.v1.login import LoginView
from library.constant.api import URL_BACKEND_API

urlpatterns = [
    path('login/', LoginView.as_view({'post': 'post'})),
    path('account/', include(URL_BACKEND_API + 'account.urls')),
    path('customer_shoes/', include(URL_BACKEND_API + 'customer_shoes.urls')),
    path('shoes/', include(URL_BACKEND_API + 'shoes.urls')),
    path('category/', include(URL_BACKEND_API + 'category.urls')),
    path('brand/', include(URL_BACKEND_API + 'brand.urls')),
    path('discount/', include(URL_BACKEND_API + 'discount.urls')),
    path('momo/', include(URL_BACKEND_API + 'momo.urls')),
]
