"""
URL configuration for fems_day_1 project.

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
from trust_rating import views  # Import views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('faculty.urls')), #Include new folder each
    path('', include('trust_rating.urls')),#Include new folder each
    path('client-history/', views.client_history, name='client_history'),
    path('trust/', include('trust_rating.urls')),  # trust_rating.urls includes this line

]
