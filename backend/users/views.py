from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from api.serializers import (
#     SubscribeSerializer
# )
# from users.serializer import PasswordSerializer, MyUserSerializer

from users.models import Subscribe, User


class SetPasswordView(APIView):
    # def post(self, request):
    #     """Изменить пароль."""
    #     serializer = PasswordSerializer(
    #         data=request.data,
    #         context={'request': request},
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {'message': 'Пароль изменен!'},
    #             status=status.HTTP_201_CREATED,
    #         )
    #     return Response(
    #         {'error': 'Введите верные данные!'},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )


class MyViewSet(UserViewSet):
    # """Пользователи и подписки."""
    # queryset = User.objects.all()
    # serializer_class = MyUserSerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    # search_fields = ('username', 'email')
    # permission_classes = (AllowAny,)

    # @action(methods=['POST', 'DELETE'], detail=True,)
    # def subscribe(self, request, id):
    #     """Подписаться отписаться."""
    #     author = get_object_or_404(User, id=id)
    #     if request.method == 'POST':
    #         if request.user.id == author.id:
    #             raise ValueError('Нельзя подписаться на себя самого')
    #         serializer = SubscribeSerializer(
    #             Subscribe.objects.create(
    #                 user=request.user,
    #                 author=author),
    #             context={'request': request})
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_201_CREATED)
    #     if request.method == 'DELETE':
    #         if Subscribe.objects.filter(
    #             user=request.user,
    #             author=author
    #         ).exists():
    #             Subscribe.objects.filter(
    #                 user=request.user,
    #                 author=author
    #                 ).delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         return Response(
    #             {'errors': 'Нельзя отписаться от автора, '
    #              'на которго вы не подписаны!'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    # @action(methods=['GET'],
    #         detail=False,
    #         permission_classes=(IsAuthenticated, )
    #         )
    # def subscriptions(self, request):
    #     """ Получить на кого пользователь подписан. """
    #     serializer = SubscribeSerializer(
    #         self.paginate_queryset(
    #             Subscribe.objects.filter(
    #                 user=request.user
    #             )),
    #         many=True, context={'request': request})
    #     return self.get_paginated_response(serializer.data)
