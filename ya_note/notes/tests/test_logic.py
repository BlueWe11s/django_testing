from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.notes_counts = Note.objects.count()
        cls.user = User.objects.create(username='Бен Афлик')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': 'Текст заметки', 'title': 'Текст заголовка',
                         'slug': 's', 'author': cls.auth_client}

    def test_user_availability_create_note(self):
        response = self.auth_client.post(reverse('notes:add'),
                                         data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        note_count = Note.objects.count()
        self.assertEqual(note_count, self.notes_counts + 1)
        note = Note.objects.last()
        self.assertEqual(note.title, 'Текст заголовка')
        self.assertEqual(note.slug, 's')
        self.assertEqual(note.text, 'Текст заметки')
        self.assertEqual(note.author, self.user)

    def test_anonymous_user_no_availability_create_note(self):
        self.client.post(reverse('notes:add'), data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.notes_counts)

    def test_no_slug(self):
        self.form_data.pop('slug')
        response = self.auth_client.post(reverse('notes:add'),
                                         data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), self.notes_counts + 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.notes_counts = Note.objects.count()
        cls.author = User.objects.create(username='Автор заметки')
        cls.note = Note.objects.create(
            title='Заголовок',
            slug='s',
            author=cls.author,
            text='Текст заметки'
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'text': 'Обновлённая заметка',
                         'title': 'Обновлённый заголовок заметки',
                         'slug': 'ns'}

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(reverse('notes:add'),
                                           data=self.form_data)
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.note.slug + WARNING))
        self.assertEqual(Note.objects.count(), self.notes_counts + 1)

    def test_author_availability_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, 'Обновлённая заметка')

    def test_author_availability_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.notes_counts)

    def test_another_user_no_availability_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, 404)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, 'Текст заметки')

    def test_another_user_no_availability_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, 404)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.notes_counts + 1)
