from django.conf import settings
from django.urls import reverse
import pytest


@pytest.mark.django_db('news')
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
    ),
)
def test_authorized_client_has_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context


@pytest.mark.django_db('news')
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
    ),
)
def test_anonymous_client_has_no_form(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
@pytest.mark.usefixtures('comment_created')
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
    ),
)
def test_comments_order(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    print(all_comments[0].created)
    assert (all_comments[0].created < all_comments[1].created)


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_count(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_order(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
