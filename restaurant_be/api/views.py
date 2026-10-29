from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .models import Category, Restaurant, Review, SavedRestaurant
from .serializers import (
    CategorySerializer,
    RestaurantSerializer,
    ReviewSerializer,
    SavedRestaurantSerializer,
    RegisterSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.select_related('category').all()
    serializer_class = RestaurantSerializer

    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ['category']
    search_fields = ['name', 'city', 'state', 'description']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related(
        'user',
        'restaurant',
    ).all()

    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant']

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']

        if Review.objects.filter(
            user=self.request.user,
            restaurant=restaurant,
        ).exists():
            raise ValidationError({
                'restaurant': (
                    'You already reviewed this restaurant. '
                    'Please edit your existing review.'
                )
            })

        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        restaurant = serializer.validated_data.get(
            'restaurant',
            serializer.instance.restaurant,
        )

        duplicate = Review.objects.filter(
            user=serializer.instance.user,
            restaurant=restaurant,
        ).exclude(pk=serializer.instance.pk).exists()

        if duplicate:
            raise ValidationError({
                'restaurant': 'You already reviewed this restaurant.'
            })

        serializer.save()


class SavedRestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = SavedRestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SavedRestaurant.objects.filter(
                user=self.request.user,
            ).select_related('restaurant')

        return SavedRestaurant.objects.none()

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']

        if SavedRestaurant.objects.filter(
            user=self.request.user,
            restaurant=restaurant,
        ).exists():
            raise ValidationError({
                'restaurant': (
                    'You already saved this restaurant. '
                    'Update its status in My Places.'
                )
            })

        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        restaurant = serializer.validated_data.get(
            'restaurant',
            serializer.instance.restaurant,
        )

        duplicate = SavedRestaurant.objects.filter(
            user=self.request.user,
            restaurant=restaurant,
        ).exclude(pk=serializer.instance.pk).exists()

        if duplicate:
            raise ValidationError({
                'restaurant': 'You already saved this restaurant.'
            })

        serializer.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    profile = getattr(request.user, 'profile', None)

    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'display_name': profile.display_name if profile else '',
    })


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = RegisterSerializer
