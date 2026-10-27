from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    RestaurantViewSet,
    ReviewViewSet,
    SavedRestaurantViewSet,
    RegisterView,
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
    path(
        'register/',
        RegisterView.as_view(),
        name='register',
    ),
    path(
        'me/',
        current_user,
        name='current-user',
    ),
    path('', include(router.urls)),
]