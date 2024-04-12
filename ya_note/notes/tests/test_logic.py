from http import HTTPStatus

from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.constants import (
    ADD_URL, DELETE_URL, EDIT_URL, SUCCESS_URL, SetUpTestData
)


class TestNoteLogic(SetUpTestData):

    def test_anonymous_user_cant_create_note(self):
        count = Note.objects.count()
        url = reverse(ADD_URL)
        self.client.post(url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, count)

    def test_user_can_create_note(self):
        initial_count = Note.objects.count()
        url = reverse(ADD_URL)
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        notes_count = Note.objects.count()
        self.assertEqual(initial_count, notes_count - 1)
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_user_cant_use_nonunique_slug(self):
        initial_count = Note.objects.count()
        url = reverse(ADD_URL)
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(url, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING)
        )
        notes_count = Note.objects.count()
        self.assertEqual(initial_count, notes_count)

    def test_empty_slug(self):
        initial_count = Note.objects.count()
        url = reverse(ADD_URL)
        del self.form_data['slug']
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        notes_count = Note.objects.count()
        self.assertEqual(initial_count, notes_count - 1)
        new_note = Note.objects.last()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_delete_note(self):
        initial_count = Note.objects.count()
        url = reverse(DELETE_URL, args=(self.note.slug,))
        response = self.auth_client.post(url)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, initial_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        initial_count = Note.objects.count()
        url = reverse(DELETE_URL, args=(self.note.slug,))
        response = self.reader_client.post(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        notes_count = Note.objects.count()
        assert notes_count == initial_count

    def test_author_can_edit_note(self):
        url = reverse(EDIT_URL, args=(self.note.slug,))
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])
        self.assertEqual(self.note.author, self.author)

    def test_user_cant_edit_note_of_another_user(self):
        url = reverse(EDIT_URL, args=(self.note.slug,))
        response = self.reader_client.post(url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, self.author)
