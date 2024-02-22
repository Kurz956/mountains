from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Mountains, Category


# Register your models here.
admin.site.site_header = 'Горная админка'
admin.site.index_title = 'RideToMountains'

class ResortFilter(admin.SimpleListFilter):
    title = 'Наличие "гостиничных комплексов"'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Рядом гостиничный комплекс'),
            ('no', 'Вокруг глушь')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(resort__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(resort__isnull=True)
@admin.register(Mountains)
class MountainsAdmin(admin.ModelAdmin):
    fields = [
        'title', 'slug', 'description','cat', 'tags', 'photo', 'mountain_photo',
        'weather', 'green', 'blue', 'red', 'black'
    ]
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields =['mountain_photo'] # ['slug'] не робит вмсте с prepopulated, только если ставить pip install unidecode
    list_display = ['id', 'title', 'description', 'date_created', 'is_published', 'cat', 'brief_info', 'mountain_photo']
    list_display_links = ['id', 'title']
    list_editable = ['is_published', 'cat']
    ordering = ['date_created', 'title']
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [ResortFilter, 'cat__name', 'is_published']
    filter_horizontal = ['tags']
    save_on_top = True

    @admin.display(description='Краткое описание', ordering='description')
    def brief_info(self, mounts:Mountains):
        return f'Описание из {len(mounts.description)} символов'

    @admin.display(description='Используемое фото')
    def mountain_photo(self, mounts:Mountains):
        if mounts.photo:
            return mark_safe(f'<img src="{ mounts.photo.url}" width=50')
        return 'Без фото'

    @admin.display(description='Опубликовать выбранное')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Mountains.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} шт.')

    @admin.display(description='Снять с публикации выбранное')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Mountains.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} шт.', messages.WARNING)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
