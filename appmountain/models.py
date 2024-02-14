from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Mountains.Status.PUBLISHED)


class Mountains(models.Model):
    class Meta:
        verbose_name = 'Гора'
        verbose_name_plural = 'Горы'
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_published = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    distance = models.IntegerField(blank=True, default=0, verbose_name='Дорога из Екб в км')
    photo = models.ImageField(upload_to='photos/', default=None, blank=True, verbose_name='Фото')
    weather = models.IntegerField(blank=True, default=0, verbose_name='Погода')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, related_name='mountains')
    tags = models.ManyToManyField('TagMountain', blank=True, related_name='tags')
    resort = models.OneToOneField('Resort', on_delete=models.SET_NULL, null=True, blank=True, related_name='mountain')

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('mountain', kwargs={'mount_slug': self.slug})

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'


    name = models.CharField(max_length=100, db_index=True, verbose_name='Рейтинг')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name




class TagMountain(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)


    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


    def __str__(self):
        return self.tag


class Resort(models.Model):
    name = models.CharField(max_length=100)
    stars = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name