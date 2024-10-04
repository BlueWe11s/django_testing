from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

from .conftest import ADMIN_CLIENT, AUTHOR_CLIENT, CLIENT


@pytest.mark.parametrize(
    'url, current_client, status', (
        (lazy_fixture('home_url'), CLIENT, HTTPStatus.OK),
        (lazy_fixture('detail_url'), CLIENT, HTTPStatus.OK),
        (lazy_fixture('login_url'), CLIENT, HTTPStatus.OK),
        (lazy_fixture('logout_url'), CLIENT, HTTPStatus.OK),
        (lazy_fixture('signup_url'), CLIENT, HTTPStatus.OK),
        (lazy_fixture('delete_comment_url'), AUTHOR_CLIENT, HTTPStatus.OK),
        (lazy_fixture('edit_comment_url'), AUTHOR_CLIENT, HTTPStatus.OK),
        (lazy_fixture('delete_comment_url'),
         ADMIN_CLIENT,
         HTTPStatus.NOT_FOUND
         ),
        (lazy_fixture('edit_comment_url'), ADMIN_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(url, current_client, status):
    response = current_client.get(url)
    assert response.status_code == status


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
def test_availability_comments_edit_and_delete(
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
