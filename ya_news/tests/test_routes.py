from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news.models import Comment, News

User = get_user_model()


# class TestRoutes(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.news = News.objects.create(title='Заголовок', text='Текст')
#         # Создаём двух пользователей с разными именами:
#         cls.author = User.objects.create(username='Лев Толстой')
#         cls.reader = User.objects.create(username='Читатель простой')
#         # От имени одного пользователя создаём комментарий к новости:
#         cls.comment = Comment.objects.create(
#             news=cls.news,
#             author=cls.author,
#             text='Текст комментария'
#         )

#     def test_pages_availability(self):
#         urls = (
#             ('news:home', None),
#             ('news:detail', (self.news.id,)),
#             ('users:login', None),
#             ('users:logout', None),
#             ('users:signup', None)
#         )
#         for name, args in urls:
#             with self.subTest(name=name):
#                 url = reverse(name, args=args)
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_availability_for_comment_edit_and_delete(self):
#         users_statuses = (
#             (self.author, HTTPStatus.OK),
#             (self.reader, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             self.client.force_login(user)
#             for name in ('news:edit', 'news:delete'):
#                 with self.subTest(user=user, name=name):
#                     url = reverse(name, args=(self.comment.id,))
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status)

#     def test_redirect_for_anonymous_client(self):
#         login_url = reverse('users:login')
#         for name in ('news:edit', 'news:delete'):
#             with self.subTest(name=name):
#                 url = reverse(name, args=(self.comment.id,))
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)

def test_home_availability_for_anonymous_user(client):
    # Адрес страницы получаем через reverse():
    url = reverse('notes:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    # Предварительно оборачиваем имена фикстур
    # в вызов функции pytest.lazy_fixture().
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, news, expected_status
):
    url = reverse(name, args=(news.slug,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture('slug_for_args')),
        ('notes:edit', pytest.lazy_fixture('slug_for_args')),
        ('notes:delete', pytest.lazy_fixture('slug_for_args')),
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
