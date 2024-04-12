from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()


HOME_URL = 'notes:home'
LIST_URL = 'notes:list'
ADD_URL = 'notes:add'
DELETE_URL = 'notes:delete'
EDIT_URL = 'notes:edit'
DETAIL_URL = 'notes:detail'
SUCCESS_URL = 'notes:success'
LOGIN_URL = 'users:login'
LOGOUT_URL = 'users:logout'
SIGNUP_URL = 'users:signup'


class SetUpTestData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note-slug',
            author=cls.author,
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
        cls.slug = (cls.note.slug,)
