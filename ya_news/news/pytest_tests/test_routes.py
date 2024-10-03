from http import HTTPStatus

from django.urls import reverse

import pytest
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects


ADMIN_CLIENT = lazy_fixture('admin_client')
AUTHOR_CLIENT = lazy_fixture('author_client')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, note_object',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ),
)
def test_pages_availability_anonymous_user(name, note_object, client):
    url = reverse(name, args=note_object)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (ADMIN_CLIENT, HTTPStatus.NOT_FOUND),
        (AUTHOR_CLIENT, HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_redirects(client, name, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
