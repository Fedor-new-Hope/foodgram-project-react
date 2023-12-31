from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

app_name = "recipes"

router = DefaultRouter()

router.register("ingredients", IngredientsViewSet, basename="ingredients")
router.register("recipes", RecipesViewSet, basename="recipes")
router.register("tags", TagsViewSet, basename="tags")

urlpatterns = [
    path("", include(router.urls)),
]
