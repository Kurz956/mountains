from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from appmountain.models import Mountains


# Create your tests here.
class GetPagesTestCase(TestCase):
    fixtures = ['appmountain_mountains.json', 'appmountain_category.json' ,
                'appmountain_resort.json' , 'appmountain_tagmountain.json' ]
    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'appmountain/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_mountain')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        mount = Mountains.published.all().select_related('cat')
        path = reverse('index')
        response = self.client.get(path)
        self.assertQuerysetEqual(mount[:5], response.context_data['posts'])

    def test_paginate_mainpage(self):
        path = reverse('index')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        mount = Mountains.published.all().select_related('cat')
        self.assertQuerysetEqual(response.context_data['posts'], mount[(page - 1) * paginate_by: page * paginate_by])


    def test_content_post(self):
        mount = Mountains.published.get(pk=1)
        path = reverse('mountain', args=[mount.slug])
        response = self.client.get(path)
        self.assertEqual(mount.description, response.context_data['mountain'].description)
    def tearDown(self):
        "Действия после выполнения каждого теста"