from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

UserModel = get_user_model()


# class ProfileEditViewTests(TestCase):
#
#
#     def test_get__expect_correct_template(self):
#         # Arrange
#         user = CustomUser.objects.create(email="test@takeaway.com", password='Ld9876kx')
#         profile = Profile.objects.get(pk=user.pk)
#         profile.first_name = 'Test'
#         profile.last_name = 'Ivanov'
#         # Act
#         response = self.client.get(reverse('edit profile',profile.pk))
#         # Assert
#         # self.assertTemplateUsed(response,'edit_profile.html')


class UserLoginViewTests(TestCase):
    def test_login_customer__expect_redirect_to_home(self):
        user_data = {
            "email": "test@takeaway.com",
            "password": "Ld9876kx",
            "is_staff": False,
            "is_superuser": False,
        }
        user = UserModel.objects.create_user(**user_data)

        self.client.login(**user_data)
        response = self.client.get(reverse("login"))
        expected_url = reverse("home")

        self.assertEqual(response.url, expected_url)

    def test_login_staff_expect_redirect_to_django_admin(self):
        user_data = {
            "email": "test@takeaway.com",
            "password": "Ld9876kx",
            "is_staff": True,
            "is_superuser": False,
        }
        user = UserModel.objects.create_user(**user_data)

        self.client.login(**user_data)
        response = self.client.get(reverse("login"))
        expected_url = reverse("admin:login")

        self.assertEqual(response.url, expected_url)
