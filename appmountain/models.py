from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Mountains.Status.PUBLISHED)


class Mountains(models.Model):
    def mountain_img_path(self, filename):
        # путь, куда будет осуществлена загрузка MEDIA_ROOT/photos/mounts/<mountain_slug>/<filename>
        return f'photos/mounts/{self.slug}/{filename}'

    class Meta:
        verbose_name = 'Гора'
        verbose_name_plural = 'Горы'
        ordering = ['title']

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug',
                            validators=[
                                MinLengthValidator(5),
                                MaxLengthValidator(100),
                            ])

    description = models.TextField(blank=True, verbose_name='Описание')
    prices = models.TextField(blank=True, verbose_name='Цены')
    tracks = models.TextField(blank=True, verbose_name='Трассы')
    work_time = models.TextField(blank=True, verbose_name='График Работы')
    season_time = models.TextField(blank=True, verbose_name='Сезон')

    is_published = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    location = models.TextField(blank=True, default='', verbose_name='Локация')

    photo = models.ImageField(upload_to=mountain_img_path, default=None, blank=True, null=True, verbose_name='Фото')
    tracks_img = models.ImageField(upload_to=mountain_img_path, default=None, blank=True, null=True, verbose_name='Схема трасс')
    weather = models.CharField(max_length=500, blank=True, default=0, verbose_name='Погода')

    red = models.IntegerField(blank=True, default=0, verbose_name='Продвинутые')
    green = models.IntegerField(blank=True, default=0, verbose_name='Учебные')
    black = models.IntegerField(blank=True, default=0, verbose_name='Сложные')
    blue = models.IntegerField(blank=True, default=0, verbose_name='Легкие')

    lift_baby = models.IntegerField(blank=True, default=0, verbose_name='Детские')
    lift_bugel = models.IntegerField(blank=True, default=0, verbose_name='Бугельные')
    lift_chair = models.IntegerField(blank=True, default=0, verbose_name='Кресельные')
    lift_cabin = models.IntegerField(blank=True, default=0, verbose_name='Кабинные')

    link = models.CharField(max_length=500, blank=True, default='', verbose_name='Линк')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, related_name='mountains', blank=True)
    tags = models.ManyToManyField('TagMountain', blank=True, related_name='tags')
    resort = models.OneToOneField('Resort', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='mountain')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='author', null=True,
                               default=None)

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
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True, default=None)


    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


    def __str__(self):
        return self.tag


class Resort(models.Model):
    class Meta:
        verbose_name = 'Курорт'
        verbose_name_plural = 'Курорты'


    name = models.CharField(max_length=100, verbose_name='Название')
    stars = models.PositiveSmallIntegerField(default=0, verbose_name='Рейтинг инфраструктуры')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, verbose_name='Описание')

    def get_absolute_url(self):
        return reverse('resort', kwargs={'resort_slug': self.slug})

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')