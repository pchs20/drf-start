from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path
from rest_framework import permissions, routers
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title='Library example project',
      default_version='v1',
      description='API for books as an example',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'books', views.BooksView)

urlpatterns = [
    path(
       'docs/',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui',
    ),
]

urlpatterns += router.urls
