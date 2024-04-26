from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/articles/', include('articles.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/chatgpt/', include('chatgpt.urls')),
]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]