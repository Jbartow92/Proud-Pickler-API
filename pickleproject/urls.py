from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from pickleapi.views import (
    PostViewSet,
    UserViewSet,
    CourtViewSet,
    CategoryViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register(r"posts", PostViewSet, basename="post")
router.register(r"courts", CourtViewSet, basename="court")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
]