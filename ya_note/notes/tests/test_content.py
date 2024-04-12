from django.urls import reverse

from notes.tests.constants import (
    ADD_URL, EDIT_URL, LIST_URL, SetUpTestData
)


class TestHomePage(SetUpTestData):

    def test_notes_list_for_non_author(self):
        url = reverse(LIST_URL)
        response = self.reader_client.get(url)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_notes_list_for_author(self):
        url = reverse(LIST_URL)
        response = self.auth_client.get(url)
        self.assertIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        urls = (
            (EDIT_URL, (self.note.slug,)),
            (ADD_URL, None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
