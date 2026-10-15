from django.contrib import admin
from .models import Category, Restaurant, Review, SavedRestaurant

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(SavedRestaurant)