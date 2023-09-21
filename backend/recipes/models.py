from django.core import validators
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(
        max_length=200, verbose_name="Название", unique=True
    )
    slug = models.SlugField(
        verbose_name="Slug",
        unique=True,
    )
    color = models.CharField(max_length=7, verbose_name="Цвет", unique=True)

    class Meta:
        ordering = ("name", "slug")
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(max_length=100, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name="Единица измерения",
    )

    class Meta:
        ordering = ("name", "measurement_unit")
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} - {self.measurement_unit}."


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        related_name="recipes",
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    image = models.ImageField(
        upload_to="recipes/images/",
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name="Описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        through="IngredientСonnetRecipe",
        related_name="recipe",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тэг",
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления",
        validators=[
            validators.MinValueValidator(
                1, "Минимальное время приготовления - 1"
            ),
            validators.MaxValueValidator(
                600, "Максимальное время приготовления - 600"
            ),
        ],
    )

    class Meta:
        ordering = ("name", "author", "cooking_time")
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.author.email}, {self.name}"


class IngredientСonnetRecipe(models.Model):
    """Модель для количества ингридиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name="ingredient",
    )
    amount = models.IntegerField(
        verbose_name="Кол-во",
        validators=[
            validators.MinValueValidator(
                1, "Минимальное количество ингредиента - 1"
            ),
            validators.MaxValueValidator(
                5000, "Максимальное количество ингредиента - 5000"
            ),
        ],
    )

    class Meta:
        ordering = ("recipe", "ingredient", "amount")
        verbose_name = "Количество ингредиентов"
        verbose_name_plural = "Количество ингредиента"
        constraints = (
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_and_ingredient",
            ),
        )


class FavoriteRecipe(models.Model):
    """Модель Избранное."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_favorite",
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="recipe_favorite",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = (
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_favorite_list_user",
            ),
        )

    def __str__(self):
        return f"{self.user.username} - {self.recipe} "


class ShoppingCart(models.Model):
    """Модель Покупка."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="shopping_cart",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="shopping_cart",
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        constraints = (
            models.UniqueConstraint(
                fields=["recipe", "user"], name="unique_cart_list_user"
            ),
        )

    def __str__(self):
        return f"{self.user} - {self.recipe.name} "
