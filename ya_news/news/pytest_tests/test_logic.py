from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

from .conftest import NEW_TEXT, TEXT


def test_user_can_create_comment(
    author_client,
    author,
    detail_url,
    new_comment,
    new
):
    comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=new_comment)
    comment = Comment.objects.get()
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == comments_count + 1
    assert comment.text == NEW_TEXT
    assert comment.news == new
    assert comment.author == author


def test_anonymous_cant_create_comment(client, detail_url, new_comment):
    comments_count = Comment.objects.count()
    client.post(detail_url, data=new_comment)
    assert Comment.objects.count() == comments_count


def test_user_cant_use_bad_words(author_client, detail_url):
    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'{TEXT}, {BAD_WORDS[0]}, {TEXT}'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == comments_count


def test_author_can_delete_comment(
    author_client,
    delete_comment_url,
    detail_url,
    comment
):
    comments_count = Comment.objects.count()
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == comments_count - 1


def test_user_cant_delete_another_comment(
    reader_client,
    delete_comment_url,
    comment
):
    comments_count = Comment.objects.count()
    response = reader_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_author_can_edit_comment(
    author_client,
    detail_url,
    edit_comment_url,
    new_comment,
    comment
):
    response = author_client.post(edit_comment_url, data=new_comment)
    comment.refresh_from_db()
    assertRedirects(response, f'{detail_url}#comments')
    assert comment.text == NEW_TEXT


def test_user_cant_edit_another_comment(
        reader_client,
        edit_comment_url,
        comment,
        new_comment,
):
    response = reader_client.post(edit_comment_url, data=new_comment)
    comment.refresh_from_db()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == TEXT
