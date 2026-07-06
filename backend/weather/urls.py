from django.urls import path
from .views import weather_proxy

urlpatterns = [
    path('', weather_proxy, name='weather_proxy'),
]
