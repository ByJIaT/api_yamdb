from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    UserViewSet,
    TitleViewSet,
    signup_view,
    token_view,
)


router_v1 = SimpleRouter()
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='сategories',
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres',
)

router_v1.register(
    r'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/signup/', signup_view, name='signup'),
    path('v1/auth/token/', token_view, name='token'),
    path('v1/', include(router_v1.urls)),
]
