"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from . import views
from django.conf.urls.static import static 
from django.conf import settings 

# contains all the urlpatterns for all the apps in the project
urlpatterns = [
    path('admin/', admin.site.urls), # admin panel
    path('',views.homepage),
    path('about/',views.about ),
    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),
    path('equipment/', include('equipment.urls')), 
    path('notifications/', include('notifications.urls')),
    path('infrastructure/', include('infrastructure.urls')), # API will now be accessible at /api/infrastructure/
    path('dashboard/', include('dashboard.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)