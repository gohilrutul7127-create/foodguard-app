from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [path('admin/', admin.site.urls), path('api/auth/', include('accounts.urls')), path('api/users/', include('users.urls')), path('api/products/', include('products.urls')), path('api/inventory/', include('inventory.urls')), path('api/notifications/', include('notifications.urls')), path('api/analytics/', include('analytics.urls')), path('api/schema/', SpectacularAPIView.as_view(), name='schema'), path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')]
