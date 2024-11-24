from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic

class TopicTests(TestCase):
    def setUp(self):
        self.topic_data = {
            'title': 'Teste de Tópico',
            'description': 'Descrição do tópico de teste',
            'author': 'testuser'
        }

    def test_create_topic_get(self):
        response = self.client.get(reverse('new_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics/new_topic.html')

    def test_create_topic_post_success(self):
        response = self.client.post(reverse('new_topic'), self.topic_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tópico criado com sucesso.')

        self.assertTrue(Topic.objects.filter(title='Teste de Tópico').exists())

    def test_create_topic_post_failure(self):
        invalid_data = {
            'title': '',
            'description': 'Descrição do tópico de teste',
            'author': 'testuser'
        }
        response = self.client.post(reverse('new_topic'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Não podem ficar campos vazios!')