from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include(('service.urls', 'service'), namespace="service")),
    path('auth/token', TokenObtainPairView.as_view(), name="token_obtain"),
    path('auth/token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('accounts/', include('allauth.urls')),
]
