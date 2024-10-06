from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from .conftest import GranTest

User = get_user_model()


class TestContent(GranTest):

    def test_notes_list(self):
        response = self.author_client.get(self.url_list)
        notes = response.context['object_list']
        self.assertIn(self.notes, notes)

    def test_notes_list_another_note(self):
        response = self.reader_client.get(self.url_list)
        notes = response.context['object_list']
        self.assertNotIn(self.notes, notes)

    def test_create_and_add_note_pages_contains_form(self):
        urls = (
            (self.url_add),
            (self.url_edit)
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
