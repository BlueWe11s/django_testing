from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='Лев Толстой'
        )
        cls.notes = Note.objects.create(title='Заголовок',
                                        text='Текст', slug='s',
                                        author=cls.author)
        cls.reader = User.objects.create(username='Читатель Простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

    def test_notes_list(self):
        url = reverse('notes:list')
        response = self.author_client.get(url)
        notes = response.context['object_list']
        self.assertIn(self.notes, notes)

    def test_notes_list_another_note(self):
        url = reverse('notes:list')
        response = self.reader_client.get(url)
        notes = response.context['object_list']
        self.assertNotIn(self.notes, notes)

    def test_create_and_add_note_pages_contains_form(self):
        urls = (
            (reverse('notes:add')),
            (reverse('notes:edit', args=(self.notes.slug,)))
        )
        for url in urls:
            response = self.author_client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
