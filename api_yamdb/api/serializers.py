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
        fields = ('name', 'year', 'description', 'id', 'genre',
                  'category', 'reviews')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title при действии 'retrieve', 'list.'"""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'id', 'genre',
                  'category', 'reviews', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    author = serializers.StringRelatedField(read_only=True)
    title = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'title', 'author', 'text', 'score',
                  'comments', 'pub_date')
        model = Review

    def validate_reviews(author, title):
        if title.reviews.filter(author=author).exists():
            raise serializers.ValidationError('Вы уже написали отзыв')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.StringRelatedField(read_only=True)
    review = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('text', 'author', 'id', 'review', 'pub_date')
        model = Comment
