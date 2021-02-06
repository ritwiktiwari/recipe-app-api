from django.test import TestCase
from django.contrib.auth import get_user_model


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
