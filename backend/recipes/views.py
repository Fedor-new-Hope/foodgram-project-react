from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets

from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# from api.filters import IngredientFilter, RecipeFilter
# from api.pagination import CustomPagination
# from api.permissions import IsAuthorOrReadOnlyPermission, ReadOnly
# from api.utils_shoping import collect_shopping_cart

# from api.serializers import (
#     IngredientSerializer,
#     GeneralSerializer,
#     RecipeSerializer,
#     TagSerializer,
# )

from recipes.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)


class TagsViewSet(ReadOnlyModelViewSet):
    """Список тэгов."""
    queryset = Tag.objects.all()
    permission_classes = (ReadOnly,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Список ингридиентов."""
    queryset = Ingredient.objects.all()
    permission_classes = (ReadOnly,)
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Список рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnlyPermission, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,)

    def new_favorite_or_cart(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = GeneralSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove_favorite_or_cart(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Рецепт уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """
        Добавить рецепт в избранное или удалить из него.
        """
        if request.method == 'POST':
            return self.new_favorite_or_cart(
                FavoriteRecipe,
                request.user,
                pk
                )
        return self.remove_favorite_or_cart(
            FavoriteRecipe,
            request.user,
            pk
            )

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Добавить рецепт в список покупок или удалить из него."""
        if request.method == 'POST':
            return self.new_favorite_or_cart(ShoppingCart, request.user, pk)
        return self.remove_favorite_or_cart(ShoppingCart, request.user, pk)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Скачать корзину (список) покупок."""
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return collect_shopping_cart(request)
