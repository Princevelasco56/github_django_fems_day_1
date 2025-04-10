# fems_day_1/urls.py
from django.contrib import admin
from django.urls import path, include  # Make sure to import include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('facultyreg/', include('facultyreg.urls')),  # Example for another app
    # path('index/', include('index.urls')),  # Example for index app
    path('client-history/', include('trust_rating.urls')),  # Add your app here
]
