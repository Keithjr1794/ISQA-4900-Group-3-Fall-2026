from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Restaurant, Review


class RestaurantAPITests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="TestPassword123!"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123!"
        )

        self.category = Category.objects.create(name="Italian")

        self.restaurant = Restaurant.objects.create(
            name="Bella Italia",
            address="123 Main Street",
            city="Omaha",
            state="NE",
            description="Italian restaurant",
            category=self.category,
            created_by=self.owner
        )

        self.client = APIClient()

    def test_get_restaurants(self):
        response = self.client.get("/api/restaurants/")
        self.assertEqual(response.status_code, 200)

    def test_create_restaurant(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post("/api/restaurants/", {
            "name": "New Restaurant",
            "address": "456 Main Street",
            "city": "Omaha",
            "state": "NE",
            "description": "Test restaurant",
            "category": self.category.id
        })

        self.assertEqual(response.status_code, 201)

        restaurant = Restaurant.objects.get(name="New Restaurant")
        self.assertEqual(restaurant.created_by, self.owner)

    def test_owner_can_update(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f"/api/restaurants/{self.restaurant.id}/",
            {"name": "Updated Restaurant"}
        )

        self.assertEqual(response.status_code, 200)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Updated Restaurant")

    def test_other_user_cannot_update(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            f"/api/restaurants/{self.restaurant.id}/",
            {"name": "Unauthorized Change"}
        )

        self.assertEqual(response.status_code, 403)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Bella Italia")

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(
            f"/api/restaurants/{self.restaurant.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Restaurant.objects.filter(id=self.restaurant.id).exists()
        )

    def test_other_user_cannot_delete(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(
            f"/api/restaurants/{self.restaurant.id}/"
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Restaurant.objects.filter(id=self.restaurant.id).exists()
        )

    def test_anonymous_cannot_create(self):
        response = self.client.post("/api/restaurants/", {
            "name": "Unauthorized Restaurant",
            "address": "123 Main Street",
            "city": "Omaha",
            "state": "NE",
            "category": self.category.id
        })

        self.assertIn(response.status_code, [401, 403])

    def test_invalid_rating(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post("/api/reviews/", {
            "restaurant": self.restaurant.id,
            "rating": 6,
            "comment": "Invalid rating"
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Review.objects.count(), 0)