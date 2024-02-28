menu = [
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить Гору", 'url_name': 'add_mountain'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]

class DataMixin:
    title_page = None
    extra_context = {'media_source_difficulty' : '/media/photos/difficulty/',
                     'media_source_lifters' : '/media/photos/lifters/',
                     'media_source_info' : '/media/photos/mounts/',
                     'map_all' : 'https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3A3d47fa26b5748430f565bb8d9d307112db23005523a0c430fec1593fcf47721d&amp;width=100%25&amp;height=640&amp;lang=ru_RU&amp;scroll=true',
                     'map_best' : 'https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3A56feaaed5cdfedd40570baba9c6a9057cfa98352c9ae2c7f472777923f0838d9&amp;width=500&amp;height=640&amp;lang=ru_RU&amp;scroll=true',
                     'map_good' : 'https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3A1a50198d26308d5be01046083286ef0ffbf33c2641787f42861692ac7627d90e&amp;width=500&amp;height=640&amp;lang=ru_RU&amp;scroll=true',
                     'map_bad' : 'https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3A387e981381ed7c7a95dc3bad68bb8ff823343d6d8bf09da708dc3587a3574766&amp;width=500&amp;height=640&amp;lang=ru_RU&amp;scroll=true',

    }
    paginate_by = 5

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu


    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        # context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
