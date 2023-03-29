from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet, GenreViewSet, ReviewViewSet, TitleViewSet
)

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
    'categories',
    CategoryViewSet,
    basename='api_yamdb_сategories',
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='api_yamdb_genres',
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
