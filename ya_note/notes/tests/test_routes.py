from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.tests.constants import (
    ADD_URL, DELETE_URL, DETAIL_URL,
    EDIT_URL, HOME_URL, LIST_URL,
    LOGIN_URL, LOGOUT_URL, SIGNUP_URL,
    SUCCESS_URL, SetUpTestData
)

User = get_user_model()


class TestRoutes(SetUpTestData):

    def test_pages_availability(self):
        urls = (
            (HOME_URL, None, self.client, HTTPStatus.OK),
            (LOGIN_URL, None, self.client, HTTPStatus.OK),
            (LOGOUT_URL, None, self.client, HTTPStatus.OK),
            (SIGNUP_URL, None, self.client, HTTPStatus.OK),
            (DETAIL_URL, self.slug, self.auth_client, HTTPStatus.OK),
            (EDIT_URL, self.slug, self.auth_client, HTTPStatus.OK),
            (DELETE_URL, self.slug, self.auth_client, HTTPStatus.OK),
            (LIST_URL, None, self.reader_client, HTTPStatus.OK),
            (ADD_URL, None, self.reader_client, HTTPStatus.OK),
            (SUCCESS_URL, None, self.reader_client, HTTPStatus.OK),
            (
                'notes:detail', self.slug,
                self.reader_client, HTTPStatus.NOT_FOUND
            ),
            (
                'notes:edit', self.slug,
                self.reader_client, HTTPStatus.NOT_FOUND
            ),
            (
                'notes:delete', self.slug,
                self.reader_client, HTTPStatus.NOT_FOUND
            ),
        )

        for name, args, client, http_status in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = client.get(url)
                self.assertEqual(response.status_code, http_status)

    def test_redirects(self):
        login_url = reverse(LOGIN_URL)
        urls = (
            (LIST_URL, None),
            (SUCCESS_URL, None),
            (ADD_URL, None),
            (DETAIL_URL, (self.note.slug,)),
            (EDIT_URL, (self.note.slug,)),
            (DELETE_URL, (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
