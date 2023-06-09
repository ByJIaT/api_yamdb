from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb import settings
from reviews.models import Category, Genre, Review, Title, Comment

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = (
            'title',
            'pub_date',
        )

    def validate_score(self, score):
        if not 1 <= score <= 10:
            raise serializers.ValidationError('Оценка в диапазоне от 1 до 10')
        return score

    def validate(self, attrs):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        if (
                request.method == 'POST'
                and Review.objects.filter(author=request.user,
                                          title=title_id).exists()
        ):
            raise serializers.ValidationError('Вы уже оставляли отзыв')

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = (
            'review',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
        lookup_field = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
        lookup_field = ('slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'genre', 'rating',
            'category', 'description',
        )
        read_only_fields = (
            'category',
            'genre',
            'rating',
        )


class TitleEditSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'genre', 'category', 'description',
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
        max_length=254,
        required=True,
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        duplicated_username = User.objects.filter(username=username).exists()
        if duplicated_username:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже зарегистрирован'
            )
        return username

    def nonadmin_update(self, instance, validated_data):
        validated_data.pop('role', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.RegexField(
        regex=settings.ALLOWED_USERNAME_RE,
        max_length=150
    )

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data['username'])
        except User.DoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user

    def validate(self, data):

        if data.get('email') and data.get('username'):
            if (
                    User.objects.filter(email=data['email']).exists()
                    and not User.objects.filter(username=data['username']
                                                ).exists()
            ):
                raise serializers.ValidationError(
                    'Недопустимая комбинация username и email.'
                )
            if User.objects.filter(username=data["username"]).exists() and (
                    User.objects.get(
                        username=data['username']).email != data['email']
            ):
                raise serializers.ValidationError(
                    'Email не соответсвует пользователю.')
        return data

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return username


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True, max_length=254)
