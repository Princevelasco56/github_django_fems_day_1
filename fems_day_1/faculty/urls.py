from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),   
    
    path('facultyreg/', views.facultyreg, name='facultyreg'),  
    path('index/', views.index, name='index'),
]

