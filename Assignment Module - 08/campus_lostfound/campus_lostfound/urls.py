"""
URL configuration for campus_lostfound project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

"""

Why two `urls.py` files?
------------------------
The project-level one is the single entry point Django checks first; 

`include('reports.urls')` hands off everything to the app's own URL file. This separation matters once a project grows to have multiple apps — each gets its own `urls.py`, and the project file just includes all of them. 

The `static(...)` lines at the bottom are only needed in development (`DEBUG = True`) — they tell Django to personally serve uploaded images and CSS files, something a real production server would normally handle instead.

"""
