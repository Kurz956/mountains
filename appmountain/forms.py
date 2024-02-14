from django import forms
from .models import Category, Resort, Mountains
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
# from django.utils.deconstruct import deconstructible




class AddMountainForm(forms.ModelForm):
    class Meta:
        model = Mountains
        fields = ['title', 'slug', 'description', 'photo', 'is_published', 'distance', 'cat', 'tags', 'resort']
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


# #
# # @deconstructible                     сейчас отрабатывает def clean_title вместо собственного валидатора
# # class RussianValidator:
# #     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- '
# #     code = 'russian'
# #
# #     def __init__(self, message=None):
# #         self.message = message if message else 'Должны присутствовать только русские символы/дефис/пробел'
# #
# #     def __call__(self, value):
# #         if not(set(value)) <= set(self.ALLOWED_CHARS):
# #             raise ValidationError(self.message, code=self.code, params={"value": value})
#
#
# class AddMountainForm(forms.Form):
#     title = forms.CharField(max_length=255, min_length=5, label="Заголовок",
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#                            #validators=[
#                            #    RussianValidator(),
#                            #],
#                             error_messages={
#                                 'min_length': 'Слишком короткий заголовок',
#                                 'required': 'Без заголовка - никак',
#                             })
#     slug = forms.SlugField(max_length=100, label='URL',
#                            validators=[
#                                MinLengthValidator(5, message="Минимум 5 символов"),
#                                MaxLengthValidator(100, message="Максимум 100 символов"),
#                            ])
#     description = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
#                                                         label='Описание')
#     is_published = forms.BooleanField(required=False, initial=True, label='Статус')
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Рейтинг отсутствует',
#                                  required=False, label='Рейтинг')
#     resort = forms.ModelChoiceField(queryset=Resort.objects.all(), empty_label='Наличие неизвестно',
#                                     required=False, label='Инфраструктура')
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны быть только русские символы, дефис и пробел.")
#
#         return title
#
#