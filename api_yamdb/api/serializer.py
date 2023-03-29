from rest_framework import serializers

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
