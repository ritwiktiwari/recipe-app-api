from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test.com', password='password'):
    """Create Sample User"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating with a new user with an email is successful"""
        email = "test@test.com"
        password = "Password123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the new user email is normalized"""
        email = "test@TEST.com"
        user = get_user_model().objects.create_user(email, "1111")

        self.assertEqual(user.email, email.lower())

    def test_new_user_required_email(self):
        """Test the new user email is required"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "1111")

    def test_new_superuser(self):
        """Test the creation of new superuser"""
        email = "test@test.com"
        password = "Password123"
        user = get_user_model().objects.create_superuser(
                email=email,
                password=password
            )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegetarian'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Corn Oil'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recpie_str(self):
        """Test the recipe string representation"""
        recpie = models.Recipe.objects.create(
            user=sample_user(),
            title='Kadhai Paneer',
            time_minutes=5,
            price=120,
        )

        self.assertEqual(str(recpie), recpie.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
