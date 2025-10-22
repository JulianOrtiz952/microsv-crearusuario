from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoyaltyPointsViewSet

router = DefaultRouter()
router.register(r'loyalty', LoyaltyPointsViewSet, basename='loyalty')

urlpatterns = [
    path('', include(router.urls)),
]
