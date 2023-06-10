"""Conferences URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Conference_data.urls')),
    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url': 'openapi/'}
    ), name='swagger-ui'),
    path('docs/openapi/', get_schema_view(
        title="Conferences project",
    ), name='openapi-schema'),
    path('api/conf_auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth-token/', include('djoser.urls.authtoken')),
    path('api/user/', include('Conference_crm.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
