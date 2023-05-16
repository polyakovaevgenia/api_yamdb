import csv

import django.db.utils
from django.core.management.base import BaseCommand

from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User


LIST_MODEL = {
    'User': {'model': User, 'file': 'static/data/users.csv'},
    'Genre': {
        'model': Genre, 'file': [
            'static/data/genre.csv', 'static/data/genre_title.csv'
        ]
    },
    'Category': {'model': Category, 'file': 'static/data/category.csv'},
    'Title': {'model': Title, 'file': 'static/data/titles.csv'},
    'Review': {'model': Review, 'file': 'static/data/review.csv'},
    'Comment': {'model': Comment, 'file': 'static/data/comments.csv'},

}


class Command(BaseCommand):

    help = 'Loads data from csv.'

    def handle(self, *args, **options):
        with open(
                LIST_MODEL['User']['file'], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                LIST_MODEL['User']['model'].objects.get_or_create(
                    pk=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row['bio'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                    },
                )

        with open(
                LIST_MODEL['Genre']['file'][0], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                LIST_MODEL['Genre']['model'].objects.get_or_create(
                    pk=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                    },
                )

        with open(
                LIST_MODEL['Genre']['file'][1], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    LIST_MODEL['Genre']['model'].objects.get(
                        pk=row['genre_id']).titles.add(row['title_id']
                                                       )
                except django.db.utils.IntegrityError:
                    continue

        with open(
                LIST_MODEL['Category']['file'], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                LIST_MODEL['Category']['model'].objects.get_or_create(
                    pk=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                    },
                )

        with open(
                LIST_MODEL['Title']['file'], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                LIST_MODEL['Title']['model'].objects.get_or_create(
                    pk=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': row['year'],
                        'category': Category.objects.get(pk=row['category']),
                    },
                )

        with open(
                LIST_MODEL['Review']['file'], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                LIST_MODEL['Review']['model'].objects.get_or_create(
                    pk=row['id'],
                    defaults={
                        'text': row['text'],
                        'author': User.objects.get(pk=row['author']),
                        'score': row['score'],
                        'pub_date': row['pub_date'],
                        'title': Title.objects.get(pk=row['title_id']),
                    },
                )

        with open(
                LIST_MODEL['Comment']['file'], 'r', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                LIST_MODEL['Comment']['model'].objects.get_or_create(
                    pk=row['id'],
                    defaults={
                        'review': Review.objects.get(
                            pk=row['review_id']
                        ),
                        'author': User.objects.get(pk=row['author']),
                        'text': row['text'],
                        'pub_date': row['pub_date'],
                    },
                )
