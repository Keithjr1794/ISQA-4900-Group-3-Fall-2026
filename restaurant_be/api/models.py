from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='restaurants'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField()
    visit_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                name='unique_user_restaurant_review'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"


class SavedRestaurant(models.Model):
    STATUS_CHOICES = [
        ('want_to_visit', 'Want to Visit'),
        ('visited', 'Visited'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='want_to_visit'
    )
    private_note = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                name='unique_saved_restaurant'
            )
        ]
