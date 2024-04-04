from datetime import datetime, timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import pytest

from news.forms import BAD_WORDS
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def news_id_for_args(news):
    return news.id,


@pytest.fixture
def comment_id_for_args(comment):
    return comment.id,


@pytest.fixture
def comment_created(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


@pytest.fixture
def bad_words_data():
    return {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    }


@pytest.fixture
def url_to_comments(news_id_for_args):
    news_url = reverse('news:detail', args=news_id_for_args)
    return news_url + '#comments'


@pytest.fixture
def edit_url(comment_id_for_args):
    return reverse('news:edit', args=comment_id_for_args)


@pytest.fixture
def delete_url(comment_id_for_args):
    return reverse('news:delete', args=comment_id_for_args)
