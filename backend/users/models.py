from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель юзера"""
    email = models.EmailField(
        help_text='Адрес электронной почты',
        max_length=254, verbose_name="Email", unique=True
    )
    username = models.CharField(
        help_text='Уникальный юзернейм',
        max_length=150,
        verbose_name="Логин",
        unique=True,
    )
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "password", "first_name", "last_name")

    class Meta:
        ordering = ("username", "email")
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username}: {self.email}."


class Subscribe(models.Model):
    """Модель Подписчик."""
    user = models.ForeignKey(
        User,
        help_text='Подписчик',
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribing",
        verbose_name="Автор",
    )

    class Meta:
        ordering = ("user", "author")
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        constraints = (
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_subscribing",
            ),
        )

    def __str__(self):
        return f"{self.user.username} - {self.author.username}"
