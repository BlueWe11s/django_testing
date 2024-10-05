import pytest
from django.conf import settings
from django.urls import reverse

from .conftest import AUTHOR_CLIENT, CLIENT, NEWS_DETAIL, NEWS_HOME


@pytest.mark.usefixtures('more_news')
def test_news_count(client):
    url = reverse(NEWS_HOME)
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.objects.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('more_news')
def test_news_order(client):
    url = reverse(NEWS_HOME)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


@pytest.mark.usefixtures('more_comment')
def test_comments_order(client, news):
    url = reverse(NEWS_DETAIL, args=(news.id,))
    response = client.get(url)
    news = response.context['news']
    all_dates = [comment.created for comment in news.comment_set.all()]
    sorted_dates = sorted(all_dates)
    assert 'news' in response.context
    assert sorted_dates == all_dates


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (AUTHOR_CLIENT, True),
        (CLIENT, False),
    )
)
def test_form_availability_for_different_clients(
    parametrized_client, note_in_list, news
):
    url = reverse(NEWS_DETAIL, args=(news.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is note_in_list
