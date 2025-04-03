from django.urls import path
from .views import register_client

urlpatterns = [
    path('register/', register_client, name='register_client'),
]
