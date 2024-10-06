from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class GranTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='Лев Толстой'
        )
        cls.reader = User.objects.create(username='Читатель простой')
        cls.notes = Note.objects.create(title='Заголовок',
                                        text='Текст', slug='s',
                                        author=cls.author)
        cls.anonimous = AnonymousUser
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.notes_counts = Note.objects.count()
        cls.form_data = {'text': 'Обновлённая заметка',
                         'title': 'Обновлённый заголовок заметки',
                         'slug': 'ns'}
        cls.url_list = reverse('notes:list')
        cls.url_add = reverse('notes:add')
        cls.url_edit = reverse('notes:edit', args=(cls.notes.slug,))
        cls.url_home = reverse('notes:home')
        cls.url_login = reverse('users:login')
        cls.url_logout = reverse('users:logout')
        cls.url_sign_up = reverse('users:signup')
        cls.url_detail = reverse('notes:detail', args=(cls.notes.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.notes.slug,))
