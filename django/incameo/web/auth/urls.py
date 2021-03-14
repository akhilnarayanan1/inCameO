"""
    URL file for Auth Page
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='web-signup'),
]