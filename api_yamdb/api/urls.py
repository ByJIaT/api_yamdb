from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api_yamdb.api.views import ReviewViewSet, UserViewSet, TitleViewSet, signup_view, token_view

router_v1 = SimpleRouter()
router_v1.register(
    'titles',
    TitleViewSet,
    basename='api_yamdb_titles',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='api_yamdb_reviews',
)

router_v1.register(
    'users',
    UserViewSet,
    basename='api_yamdb_users'
)

urlpatterns = [
    path('v1/auth/signup/', signup_view, name='signup'),
    path('v1/auth/token/', token_view, name='token'),
    path('v1/', include(router_v1.urls))
]
