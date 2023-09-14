from django.contrib import admin

from recipes.models import (
    Ingredient,
    IngredientInRecipe,
    FavoriteRecipe,
    Recipe,
    ShoppingCart,
    Tag
)


admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Recipe)
admin.site.register(FavoriteRecipe)
admin.site.register(IngredientInRecipe)
admin.site.register(Ingredient)
