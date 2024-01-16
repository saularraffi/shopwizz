from django.urls import path 
from . import views

urlpatterns = [
    path('', views.getData),
    path('test', views.getTest),
    path('test2', views.getTest2),
    path('urls', views.getUrls),
]