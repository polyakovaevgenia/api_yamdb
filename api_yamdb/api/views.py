from rest_framework import filters, mixins, viewsets, serializers
from django.db.models import Avg
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review

from .filters import FilterForTitles
from .serializers import (CategorySerializer, GenreSerializer,
                          ReadOnlyTitleSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer
                          )
from .permissions import (RoleAdminrOrReadOnly,
                          IsAdminIsModeratorIsAuthorOrReadOnly)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """API для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (RoleAdminrOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """API для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (RoleAdminrOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """API для работы c произведениями."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    permission_classes = (RoleAdminrOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterForTitles
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """API для работы c отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminIsModeratorIsAuthorOrReadOnly,)

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        title = self.get_title()
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        try:
            title = self.get_title()
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'Вы можете оставить только один отзыв.'})
        return title


class CommentViewSet(viewsets.ModelViewSet):
    """API для работы c комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminIsModeratorIsAuthorOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
