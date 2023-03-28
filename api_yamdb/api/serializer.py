from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.api.validators import RangeValueValidator
from api_yamdb.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = (
            'title_id',
            'author',
            'pub_date',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title_id', 'author']
            ),
            RangeValueValidator(
                field='score',
            ),

        ]
