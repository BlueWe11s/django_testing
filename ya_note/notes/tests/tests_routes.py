from http import HTTPStatus

from django.urls import reverse

from .conftest import GranTest


class TestRoutes(GranTest):

    def test_availability_pages(self):
        urls = (
            [self.url_home, self.anonimous, HTTPStatus.OK]
            [self.url_login, self.anonimous, HTTPStatus.OK]
            [self.url_logout, self.anonimous, HTTPStatus.OK]
            [self.url_sign_up, self.anonimous, HTTPStatus.OK]
            [self.url_detail, self.author, HTTPStatus.OK]
            [self.url_delete, self.author, HTTPStatus.OK]
            [self.url_edit, self.author, HTTPStatus.OK]
            [self.url_detail, self.reader, HTTPStatus.NOT_FOUND]
            [self.url_delete, self.reader, HTTPStatus.NOT_FOUND]
            [self.url_edit, self.reader, HTTPStatus.NOT_FOUND]
            [self.url_succes, self.author, HTTPStatus.FOUND]
            [self.url_add, self.author, HTTPStatus.FOUND]
            [self.url_list, self.author, HTTPStatus.FOUND]
        )
        for url, user, status in urls:
            with self.subTest(user=user, name=url):
                url = reverse(url)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_anonymous_client(self):
        urls = (self.url_list,
                self.url_detail,
                self.url_edit,
                self.url_add,
                self.url_delete)
        for url in urls:
            with self.subTest(name=url):
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
