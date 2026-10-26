from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    RestaurantViewSet,
    ReviewViewSet,
    SavedRestaurantViewSet,
    current_user,
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
    path('me/', current_user, name='current-user'),
    path('', include(router.urls)),
]