from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects
import pytest

from news.forms import WARNING
from news.models import Comment


def test_user_can_create_note(
    author_client,
    author,
    form_data,
    news_id_for_args,
    news
):
    url = reverse('news:detail', args=(news_id_for_args))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client, form_data, news_id_for_args):
    count = Comment.objects.count()
    url = reverse('news:detail', args=(news_id_for_args))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == count


def test_user_cant_use_bad_words(
    author_client,
    news_id_for_args,
    bad_words_data
):
    count = Comment.objects.count()
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == count


def test_author_can_edit_comment(
    author_client, form_data,
    comment,
    edit_url,
    url_to_comments
):
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(
    admin_client,
    form_data,
    comment,
    edit_url
):
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(author_client, delete_url, url_to_comments):
    count = Comment.objects.count() - 1
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == count


def test_other_user_cant_delete_comment(admin_client, delete_url):
    count = Comment.objects.count()
    response = admin_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count
