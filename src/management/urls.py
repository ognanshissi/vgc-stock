"""management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import re_path, path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomepageView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', HomepageView.as_view(), name='home'),

    # account URLS
    re_path(r'^account/', include('account.urls', namespace='account')),
    re_path(r'^lens/', include('lens.urls', namespace='lens'))
]

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]

# Include Media and static files when DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
