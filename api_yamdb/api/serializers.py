from rest_framework import serializers

from reviews.models import (Category,
                            Genre,
                            Title,
                            Review,
                            Comment
                            )


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title при действии 'retrieve', 'list.'"""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
