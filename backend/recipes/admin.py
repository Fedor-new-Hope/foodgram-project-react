from django.contrib import admin
from recipes.models import (FavoriteRecipe, Ingredient, IngredientСonnetRecipe,
                            Recipe, ShoppingCart, Tag)


class RecipeIngredientsAdmin(admin.StackedInline):
    model = IngredientСonnetRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsAdmin,)
    list_display = ("author", "name", "text")
    search_fields = (
        "name",
        "cooking_time",
        "author__username",
        "ingredients__name",
    )
    empty_value_display = "-пусто-"
    list_filter = ("author", "name", "tags")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(FavoriteRecipe)
