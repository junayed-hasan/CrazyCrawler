from django.contrib import admin
from django.urls import path, include

#this tells the browser that if the url is extended to 'page/' then it takes us to that page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search_engine.urls')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
