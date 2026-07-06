from django.urls import path
from .views import poll_notifications, mark_read

urlpatterns = [
    path('poll/', poll_notifications, name='poll_notifications'),
    path('mark-read/', mark_read, name='mark_read'),
]
