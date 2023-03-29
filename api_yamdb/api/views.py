from django.db.models.aggregates import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import IsAuthorOrReadOnly
from api.serializer import (
    CategorySerializer, GenreSerializer, ReviewSerializer,
    TitleEditSerializer, TitleReadSerializer
)
from reviews.models import Category, Genre, Title


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
    pagination_class = LimitOffsetPagination
    # место для permission_classes
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleEditSerializer
        return TitleReadSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    # место для permission_classes
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    # место для permission_classes
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
