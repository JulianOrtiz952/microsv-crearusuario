from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailLogViewSet

router = DefaultRouter()
router.register(r'emails', EmailLogViewSet, basename='email')

urlpatterns = [
    path('', include(router.urls)),
]
