from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet

router_v1 = SimpleRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='api_yamdb_reviews',
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
