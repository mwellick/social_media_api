import pathlib
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def user_profile_image_path(instance: "User", filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.username)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/users") / pathlib.Path(filename)


class User(AbstractUser):
    username = models.CharField(max_length=63, unique=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        blank=True, null=True, upload_to=user_profile_image_path
    )
    online = models.BooleanField(default=False)
    user_followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="follow_users", blank=True
    )
    user_following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="following_users", blank=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
