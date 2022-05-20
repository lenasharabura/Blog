from django.test import TestCase
from django.urls import reverse

from accounts.forms import User
from articles.models import Article


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article1 = Article.objects.create(
            name="Test Article 1",
            article="Test text for our article",
        )
        self.home_page_url = reverse("home")
        self.save_article = reverse("save_article")

    def test_save_article(self):
        response = self.client.post(self.save_article)
        self.assertEqual(self.article1.save(), True)

    # def test_home_page_status_code(self):
    #     response = self.client.get(self.home_page_url)
    #     self.assertEqual(response.status_code, 200)
