from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create and return sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 1000,
        'link': 'google.com'
    }
    defaults.update(**params)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
    """Test the publicly availabe recipe API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retreving recipes"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test the authorized recipe API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retreive_recipes(self):
        """Test retreiving recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')
        serailizer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serailizer.data)

    def test_recipes_limited_to_user(self):
        """Test that the recipes is returned to the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='test2@test.com',
            password='password'
        )

        sample_recipe(user=user2)

        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    # def test_create_recipes_successful(self):
    #     """Test creating a new recipe"""
    #     payload = {
    #     'title': 'Sample recipe',
    #     'time_minutes': 10,
    #     'price': 1000
    #     }
    #     self.client.post(RECIPES_URL, payload)

    #     exists = Recipe.objects.filter(
    #         user=self.user,
    #         title=payload['title']
    #     ).exists()

    #     self.assertTrue(exists)

    # def test_create_recipe_invalid(self):
    #     """Test creating recipe with invalid payload"""
    #     payload = {'title': ''}
    #     res = self.client.post(RECIPES_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
