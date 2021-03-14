"""
    URL file for All Web Page
"""
from django.urls import path, include

urlpatterns = [
    path('', include('web.auth.urls')),
]