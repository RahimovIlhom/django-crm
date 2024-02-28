from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version='v1',
        description="Django academy CRM",
        terms_of_service="No url service",
        contact=openapi.Contact(email="ilhomjonrahimov217@gmail.com"),
        license=openapi.License(name="Django academy License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/courses/', include('course.urls')),
    path('api/customer/', include('customer.urls')),
    path('api/groups/', include('group.urls')),
    path('api/payments/', include('payment.urls')),
    path('api/attendances/', include('attendance.urls')),
    path('api/token/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
