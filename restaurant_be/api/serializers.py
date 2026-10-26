from rest_framework import serializers
from .models import Category, Restaurant, Review, SavedRestaurant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True,
    )

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['created_by']


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']


class SavedRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedRestaurant
        fields = '__all__'
        read_only_fields = ['user']