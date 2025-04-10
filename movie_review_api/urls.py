"""
URL configuration for movie_review_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"message": "Welcome to Movie Review API. Go to /api/v1/docs/ for docs."})

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Review API",
        default_version='v1',
        description="API documentation description",
        terms_of_service="https://www.mreview.com/terms/",
        contact=openapi.Contact(email="support@mreview.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


# API v1 url patterns
api_v1_patterns = [
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('movies/', include('movies.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_patterns)),
]
