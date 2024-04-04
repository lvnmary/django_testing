from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestHomePage(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            author=cls.author,
            text='Текст комментария',
            title='Заголовок',
            slug='slug'
        )

    def test_notes_list_for_author_users(self):
        users_statuses = (
            (self.author, True),
            (self.reader, False),
        )
        for user, statuse in users_statuses:
            self.client.force_login(user)
            response = self.client.get(self.LIST_URL)
            object_list = response.context['object_list']
            if statuse:
                self.assertIn(self.note, object_list)
            else:
                self.assertNotIn(self.note, object_list)

    def test_pages_contains_form(self):
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
