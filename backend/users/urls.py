from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import MyViewSet, SetPasswordView

app_name = "users"

router = DefaultRouter()

router.register("users", MyViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("users/set_password/", SetPasswordView, name="set_password"),
    path("auth/", include("djoser.urls.authtoken"), name="auth"),
]
