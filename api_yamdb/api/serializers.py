from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Title, Review
from users.models import User


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
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')

    def to_representation(self, instance):
        return ReadOnlyTitleSerializer(instance).data

    def validate(self, data):
        if 'genre' in data and not len(data['genre']):
            raise serializers.ValidationError(
                'Поле genre обязательно к заполнению!'
            )
        return data


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Title при действии 'retrieve', 'list.'"""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'title', 'author', 'text', 'score',
                  'comments', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('text', 'author', 'id', 'review', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя - Администратор"""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]+\Z',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserRegistrering(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]+\Z',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.casefold() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me в качестве username запрещено'
            )
        return value


class TokenJWTSerializer(serializers.Serializer):
    """"Сериалайзер для получения токена"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с личными данными поьзователя."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(regex=r'^[\w.@+-]+\Z',
                           message='Неверное имя пользователя')
        ),
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),),
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
