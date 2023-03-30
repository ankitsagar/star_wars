"""star_wars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


API_BASE_PATH = "api/v1/"

schema_view = get_schema_view(
   openapi.Info(
      title="Star wars API",
      default_version='v1',
      description="APIs to fetch planet and movies of start wars series",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_BASE_PATH + "docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(API_BASE_PATH + "planets/", include('planets.urls')),
    path(API_BASE_PATH + "movies/", include('movies.urls')),
]
