from django.contrib.auth import get_user_model
from django.test import TestCase  # upgrade unittest.TestCase

from accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    # setup
    PROFILE_VALID_FIRST_NAME = "Test"
    PROFILE_VALID_LAST_NAME = "Ivanov"
    PROFILE_EMPTY_FIRST_NAME = None
    PROFILE_EMPTY_LAST_NAME = None

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(
            first_name=self.PROFILE_VALID_FIRST_NAME,
            last_name=self.PROFILE_VALID_LAST_NAME,
        )
        expected_full_name = (
            f"{self.PROFILE_VALID_FIRST_NAME} {self.PROFILE_VALID_LAST_NAME}"
        )
        self.assertEqual(expected_full_name, profile.full_name)

    def test_profile_full_name__when_no_first_name__expect_exactly_last_name(self):
        profile = Profile(
            first_name=self.PROFILE_EMPTY_FIRST_NAME,
            last_name=self.PROFILE_VALID_LAST_NAME,
        )
        expected_full_name = f"{self.PROFILE_VALID_LAST_NAME}"
        self.assertEqual(expected_full_name, profile.full_name)

    def test_profile_full_name__when_no_last_name__expect_exactly_first_name(self):
        profile = Profile(
            first_name=self.PROFILE_VALID_FIRST_NAME,
            last_name=self.PROFILE_EMPTY_LAST_NAME,
        )
        expected_full_name = f"{self.PROFILE_VALID_FIRST_NAME}"
        self.assertEqual(expected_full_name, profile.full_name)

    def test_profile_create__when_user_created__expect_empty_profile(self):
        user = UserModel.objects.create(email="test@takeaway.com", password="Ld9876kx")
        profile = Profile.objects.get(pk=user.pk)
        self.assertEqual(profile.full_name, "No name")

    def test_profile_image_upload_S3(self):
        pass
