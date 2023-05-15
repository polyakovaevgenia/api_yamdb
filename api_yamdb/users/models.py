from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )
    
    username = models.CharField(
        max_length=150,
        verbose_name='Username',
        unique=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        blank=False,
        null=False,
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        null=True)
    
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        null=True)
    
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
        default=None,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=USER,
        blank=False,
        max_length=15,
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['role', 'username']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
