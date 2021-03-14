"""
    URLs file to manage Auth
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import AuthFacebook,AuthGoogle,SignupViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register('signup', SignupViewset, basename='auth_signup')


urlpatterns = [
    path('', include(router.urls)),

    path('token/get/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('facebook/', AuthFacebook.as_view()),
    path('google/', AuthGoogle.as_view()),
]