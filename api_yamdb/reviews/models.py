from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validator_year
from users.models import User

TEXT_SYMBOLS_NUMBER = 25
MINIMAL_SCORE = 1
MAXIMUM_SCORE = 10


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату публикации при создании."""

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время публикации',
        help_text='Автоматическое добавление при публикации',
    )

    class Meta:
        abstract = True


class Category(models.Model):
    """Модель Категории для произведения."""

    name = models.CharField(
        verbose_name='Категория',
        help_text='Наименование категории',
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Короткое наименование',
        help_text='Короткое наименование (например, для категории '
                  'фильмы slug будет films).',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель Жанра для произведения."""

    name = models.CharField(
        verbose_name='Жанр',
        help_text='Наименование жанра',
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Короткое наименование',
        help_text='Короткое наименование (например, для жанра '
                  'ужасы slug будет horror).',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель Произведения."""

    name = models.CharField(
        verbose_name='Произведение',
        help_text='Наименование произведения',
        max_length=128,
    )
    year = models.PositiveIntegerField(
        verbose_name='Год',
        help_text='Год создания произведения',
        validators=(validator_year,),
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Краткое описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Жанр произведения',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Категория произведения',
        related_name='titles',
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', 'year')

    def __str__(self):
        return self.name


class Review(CreatedModel):
    """Модель Отзывы для произведения."""

    title = models.ForeignKey(
        Title,
        verbose_name='Отзыв',
        help_text='Наименование произведения для отзыва',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор отзыва',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(MINIMAL_SCORE),
            MaxValueValidator(MAXIMUM_SCORE)
        ]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']

    def __str__(self):
        return self.text[:TEXT_SYMBOLS_NUMBER]


class Comment(CreatedModel):
    """Модель Комментариев для отзыва."""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        help_text='Отзыв, на который написан комментарий',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор комментария',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_SYMBOLS_NUMBER]
