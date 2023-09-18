from api.core_image import Base64ImageField
from recipes.models import (FavoriteRecipe, Ingredient, IngredientСonnetRecipe,
                            Recipe, ShoppingCart, Tag)
from rest_framework import serializers, validators
from rest_framework.generics import get_object_or_404
from users.models import Subscribe, User
from users.serializer import MyUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientСonnetRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientСonnetRecipe
        fields = ("id", "name", "measurement_unit", "amount")

        validators = [
            validators.UniqueTogetherValidator(
                queryset=IngredientСonnetRecipe.objects.all(),
                fields=("ingredient", "recipe"),
            )
        ]


class UserRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")

        read_only_fields = ("id", "name", "image", "cooking_time")


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="author.id")
    email = serializers.EmailField(source="author.email")
    username = serializers.CharField(source="author.username")
    first_name = serializers.CharField(source="author.first_name")
    last_name = serializers.CharField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
        )

        read_only_fields = ("is_subscribed",)

    def validate(self, data):
        user_id = data["user_id"]
        author_id = data["author_id"]
        if user_id == author_id:
            raise serializers.ValidationError(
                {"errors": "Нельзя подписаться на самого себя."}
            )
        if Subscribe.objects.filter(user=user_id, author=author_id).exists():
            raise serializers.ValidationError(
                {"errors": "Нельзя подписаться повторно."}
            )
        data["user"] = get_object_or_404(User, id=user_id)
        data["author"] = get_object_or_404(User, id=author_id)
        return data

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes_limit = request.GET.get("recipes_limit")
        recipes = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = UserRecipeSerializer(recipes, many=True)
        return serializer.data


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()
    ingredients = IngredientСonnetRecipeSerializer(
        many=True, read_only=True, source="recipe_ingredients"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
        )

    @staticmethod
    def ingredients_recipe_add(recipe, ingredients):
        IngredientСonnetRecipe.objects.bulk_create(
            [
                IngredientСonnetRecipe(
                    recipe=recipe,
                    ingredient_id=ingredient.get("id"),
                    amount=ingredient.get("amount"),
                )
                for ingredient in ingredients
            ]
        )

    def create(self, validated_data):
        image = validated_data.pop("image")
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.ingredients_recipe_add(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.tags.set(validated_data.pop("tags"))
        IngredientСonnetRecipe.objects.filter(recipe=instance).delete()
        self.ingredients_recipe_add(
            recipe=instance, ingredients=validated_data.pop("ingredients")
        )
        super().update(instance, validated_data)
        return instance

    def to_internal_value(self, data):
        ingredients = data.pop("ingredients")
        tags = data.pop("tags")
        data = super().to_internal_value(data)
        data["tags"] = tags
        data["ingredients"] = ingredients
        return data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        return (request and request.user.is_authenticated
                and ShoppingCart.objects.filter(
                    recipe=obj, user=request.user).exists())

    def validate(self, data):
        ingredients = data.get("ingredients")
        tags = data.get("tags")
        if not tags:
            raise serializers.ValidationError(
                {"tags": "Нужно выбрать хотя бы один тег!"}
            )
        if not ingredients:
            raise serializers.ValidationError(
                {"ingredients": "Нужен хотя бы один ингредиент!"}
            )
        added_ingredients = []
        for ingredient in ingredients:
            if int(ingredient["amount"]) < 1:
                raise serializers.ValidationError(
                    {"amount": "Количество ингредиента должно быть больше 1!"}
                )
            if ingredient["id"] in added_ingredients:
                raise serializers.ValidationError(
                    {"ingredients": "Ингридиенты не могут повторяться!"}
                )
            added_ingredients.append(ingredient["id"])
        cooking_time = float(data.get("cooking_time"))
        if cooking_time < 1:
            raise serializers.ValidationError(
                {
                    "cooking_time":
                    "Время приготовления должно быть не меньше 1 минуты"
                }
            )
        if cooking_time > 600:
            raise serializers.ValidationError(
                {
                    "cooking_time":
                    "Время приготовления должно быть не больше 600 минут"
                }
            )
        data["ingredients"] = ingredients
        data["tags"] = tags
        return data
