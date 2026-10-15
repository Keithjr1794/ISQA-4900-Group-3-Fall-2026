from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .permissions import IsOwnerOrReadOnly
from .models import Category, Restaurant, Review, SavedRestaurant
from .serializers import (
    CategorySerializer,
    RestaurantSerializer,
    ReviewSerializer,
    SavedRestaurantSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedRestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = SavedRestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SavedRestaurant.objects.filter(user=self.request.user)
        return SavedRestaurant.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
