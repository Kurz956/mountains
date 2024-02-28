from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    def user_img_path(self, filename):
        # путь, куда будет осуществлена загрузка MEDIA_ROOT/users/{self.username}/{filename}
        return f'users/{self.username}/{filename}'


    photo = models.ImageField(upload_to=user_img_path, blank=True, null=True, verbose_name='Фотография')
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')