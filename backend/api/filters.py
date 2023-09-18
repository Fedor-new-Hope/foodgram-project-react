from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, FilterSet)
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    search_param = "name"


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    is_favorited = BooleanFilter(
        field_name="is_favorited", method="filter_favorited"
    )
    is_in_shopping_cart = BooleanFilter(
        field_name="is_in_shopping_cart", method="filter_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = ("author",)

    def filter_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(recipe_favorite__user=self.request.user)
        return queryset

    def filter_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
