from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Notes API",
      default_version='v1',
      description="API documentation for Notes CRUD API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourdomain.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/notes/", include('notes.urls', namespace='notes')),
    path("api/auth/", include('authentication.urls', namespace='authentication')),
    
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
]
