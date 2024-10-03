from datetime import timedelta

import pytest
from pytest_lazyfixture import lazy_fixture
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

ANONYMOUS = lazy_fixture('client')
AUTHOR = lazy_fixture('author_client')
READER = lazy_fixture('reader_client')

TITLE = 'Заголовок'
TEXT = 'Текст'
NEW_TEXT = 'Новый текст'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        username='Кайл Брафловски',
        password='jussword')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(
        username='Эрик Картман',
        password='fassword')


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title=TITLE,
        text=TEXT,
    )
    return news


@pytest.fixture
def bulk_news_creation(author):
    return News.objects.bulk_create(
        News(
            title=f'{TITLE} {index}',
            text=TEXT,
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        author=author,
        news=news,
        text=TEXT
    )
    return comment


@pytest.fixture
def multiple_comments(author, news):
    for index in range(3):
        comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'{TEXT} {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def new_comment():
    return {'text': NEW_TEXT}


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
