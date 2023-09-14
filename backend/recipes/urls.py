from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import (
    IngredientsViewSet,
    RecipesViewSet,
    TagsViewSet,
)

app_name = 'recipes'

router = DefaultRouter()

router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')

urlpatterns = [path('', include(router.urls)), ]
