from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from django.urls import reverse
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Mountains.Status.PUBLISHED)

class Mountains(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=100, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_published =  models.PositiveSmallIntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    distance = models.IntegerField(blank=True, default=0)
    photo = models.ImageField(upload_to='photos/', default=None, blank=True, verbose_name='Фото')
    weather = models.IntegerField(blank=True, default=0)
    rating = models.IntegerField(blank=True, default=0)

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('mountain', kwargs={'mount_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Гора'
        verbose_name_plural = 'Горы'

