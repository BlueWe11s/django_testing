from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()


class Test(TestCase):
    AUTHOR_USER = 'Лев Толстой'
    READER_USER = 'Читатель простой'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='Лев Толстой'
        )
        cls.notes = Note.objects.create(title='Заголовок',
                                        text='Текст', slug='s',
                                        author=cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
