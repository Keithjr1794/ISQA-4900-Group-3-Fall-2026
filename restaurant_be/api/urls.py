from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    RestaurantViewSet,
    ReviewViewSet,
    SavedRestaurantViewSet,
)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(
    r'saved-restaurants',
    SavedRestaurantViewSet,
    basename='saved-restaurant',
)

urlpatterns = [
    path('', include(router.urls)),
]