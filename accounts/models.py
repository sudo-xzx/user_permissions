from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    first_name = models.CharField("имя", max_length=150, blank=True)
    last_name = models.CharField("фамилия", max_length=150, blank=True)

    is_active = models.BooleanField("активен", default=True)
    is_staff = models.BooleanField("статус персонала", default=False)
    date_joined = models.DateTimeField("дата регистрации", default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        return self.first_name or self.email


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="пользователь",
    )
    avatar = models.ImageField("аватар", upload_to="avatars/", blank=True, null=True)
    city = models.CharField("город", max_length=100, blank=True)
    bio = models.TextField("описание", max_length=500, blank=True)
    updated_at = models.DateTimeField("обновлён", auto_now=True)

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.email}"

    def is_complete(self):
        return bool(self.city and self.bio)
