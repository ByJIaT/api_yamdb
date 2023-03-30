from django.db.models.aggregates import Avg
from django_filters import rest_framework as filters
from http import HTTPStatus

from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters, viewsets

from api.filters import TitleFilter

from api_yamdb.api.utils import send_confirmation_mail
from api_yamdb.api.permissions import IsAuthorOrReadOnly, IsAdmin
from api_yamdb.api.serializer import (ReviewSerializer,
                                      GetCodeSerializer,
                                      GetTokenSerializer,
                                      UserSerializer,
                                      CommentSerializer,
                                      TitleEditSerializer, 
                                      TitleReadSerializer)
from api_yamdb.reviews.models import Title

from users.models import User
from reviews.models import Title, Review


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        pk = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=pk)
        return title

    def get_queryset(self):
        return self.get_title().reviews_review

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review(self):
        pk = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=pk)
        return review

    def get_queryset(self):
        return self.get_review().reviews_comment

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)


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

class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        ['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path='me',
    )
    def user_selfview(self, request):
        """Вьюфункция собвственного профиля."""
        if not request.data:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=HTTPStatus.OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.user.is_admin:
            serializer.update(request.user, serializer.validated_data)
        else:
            serializer.nonadmin_update(request.user, serializer.validated_data)

        return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """Вью регистрации и входа."""
    serializer = GetCodeSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
    except Exception:
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    user = serializer.save()
    confirmation_code = send_confirmation_mail(user)
    User.objects.filter(username=user.username).update(
        confirmation_code=confirmation_code
    )

    return Response(request.data, status=HTTPStatus.OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def token_view(request):
    """Вью токена работы с API по коду подтверждения."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)

        return Response({'token': f'{token}'}, status=HTTPStatus.OK)

    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=HTTPStatus.BAD_REQUEST,
    )

