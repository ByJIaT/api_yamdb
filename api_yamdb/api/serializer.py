from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.validators import RangeValueValidator
from reviews.models import Category, Genre, Review, Title, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = (
            'title',
            'author',
            'pub_date',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author']
            ),
            RangeValueValidator(
                field='score',
            ),
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = (
            'review',
            'author',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = ('slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'
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
        fields = '__all__'
