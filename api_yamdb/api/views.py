from django.db.models.aggregates import Avg
from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from .filters import TitleFilter
from .permissions import IsAuthorOrReadOnly
from .serializer import ReviewSerializer, TitleEditSerializer, TitleReadSerializer
from reviews.models import Title


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        pk = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        return title

    def get_queryset(self):
        return self.get_title().api_yamdb_reviews

    def perform_create(self, serializer):
        serializer.save(title_id=self.get_title(), author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(title_id=self.get_title(), author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete(title_id=self.get_title(), author=self.request.user)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews_review__score')
    )
    # место для permission_classes
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleEditSerializer
        return TitleReadSerializer
