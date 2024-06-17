from django.urls import path, include
from rest_framework import routers
from .views import (
    PostViewSet,
    CommentViewSet,
    LikeViewSet,
    FollowViewSet,
    UnfollowViewSet
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet)
router.register("follows", FollowViewSet)
router.register("unfollows", UnfollowViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "social_media_api"
