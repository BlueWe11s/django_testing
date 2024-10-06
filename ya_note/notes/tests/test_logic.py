from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .conftest import GranTest

User = get_user_model()


class TestNoteCreation(GranTest):

    def test_user_availability_create_note(self):
        response = self.reader_client.post(self.url_add,
                                           data=self.form_data)
        note_count = Note.objects.count()
        note = Note.objects.last()
        self.assertRedirects(response, self.url_succes)
        self.assertEqual(note_count, self.notes_counts + 1)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.reader)

    def test_anonymous_user_no_availability_create_note(self):
        self.client.post(self.url_add, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.notes_counts)

    def test_no_slug(self):
        self.form_data.pop('slug')
        response = self.reader_client.post(self.url_add,
                                           data=self.form_data)
        new_note = Note.objects.last()
        expected_slug = slugify(self.form_data['title'])
        self.assertRedirects(response, self.url_succes)
        self.assertEqual(Note.objects.count(), self.notes_counts + 1)
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(GranTest):

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.notes.slug
        response = self.author_client.post(self.url_add,
                                           data=self.form_data)
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.notes.slug + WARNING))
        self.assertEqual(Note.objects.count(), 1)

    def test_author_availability_edit_note(self):
        response = self.author_client.post(self.url_edit, data=self.form_data)
        self.notes.refresh_from_db()
        self.assertRedirects(response, self.url_succes)
        self.assertEqual(self.notes.text, self.form_data['text'])

    def test_author_availability_delete_note(self):
        response = self.author_client.post(self.url_add,
                                           data=self.form_data)
        response = self.author_client.delete(self.url_delete)
        notes_count = Note.objects.count()
        self.assertRedirects(response, self.url_succes)
        self.assertEqual(notes_count, self.notes_counts)

    def test_another_user_no_availability_edit_note_of_another_user(self):
        response = self.reader_client.post(self.url_edit, data=self.form_data)
        self.notes.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.notes.text, 'Текст')

    def test_another_user_no_availability_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.url_delete)
        notes_count = Note.objects.count()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_count, 1)
