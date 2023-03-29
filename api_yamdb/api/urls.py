from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import ReviewViewSet, TitleViewSet, CommentViewSet

router_v1 = SimpleRouter()
router_v1.register(
    'titles',
    TitleViewSet,
    basename='api_yamdb_titles',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
