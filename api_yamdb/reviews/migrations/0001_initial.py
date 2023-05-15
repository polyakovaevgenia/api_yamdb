import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование категории', max_length=128, unique=True, verbose_name='Категория')),
                ('slug', models.SlugField(help_text='Короткое наименование (например, для категории фильмы slug будет films).', unique=True, verbose_name='Короткое наименование')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Автоматическое добавление при публикации', verbose_name='Дата и время публикации')),
                ('text', models.TextField(help_text='Текст комментария', verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование жанра', max_length=128, unique=True, verbose_name='Жанр')),
                ('slug', models.SlugField(help_text='Короткое наименование (например, для жанра ужасы slug будет horror).', unique=True, verbose_name='Короткое наименование')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Автоматическое добавление при публикации', verbose_name='Дата и время публикации')),
                ('text', models.TextField(help_text='Текст отзыва', verbose_name='Текст')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование произведения', max_length=128, verbose_name='Произведение')),
                ('year', models.PositiveIntegerField(help_text='Год создания произведения', validators=[reviews.validators.validator_year], verbose_name='Год')),
                ('rating', models.IntegerField(blank=True, help_text='Рейтинг произведения от пользователей', null=True, verbose_name='Рейтинг произведения')),
                ('description', models.TextField(blank=True, help_text='Краткое описание произведения', null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(help_text='Категория произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Жанр произведения', related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ['name', 'year'],
            },
        ),
    ]
