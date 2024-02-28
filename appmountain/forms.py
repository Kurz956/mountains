from django import forms
from .models import Category, Resort, Mountains
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
# from django.utils.deconstruct import deconstructible




class AddMountainForm(forms.ModelForm):
    class Meta:
        model = Mountains
        fields = ['title', 'slug', 'description', 'photo', 'is_published', 'cat', 'tags', 'resort']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Рейтинг отсутствует',
                                 required=False, label='Рейтинг')
    resort = forms.ModelChoiceField(queryset=Resort.objects.all(), empty_label='Наличие неизвестно',
                                    required=False, label='Инфраструктура')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        elif not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")
        return title

class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Изображение')
