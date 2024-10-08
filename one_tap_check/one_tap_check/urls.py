"""
URL configuration for one_tap_check project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import notifications.urls
from dashboard.views import home_page
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('one_tap_api/', include('one_tap_api.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('<path:not_found>', RedirectView.as_view(url='/home/')),
]
