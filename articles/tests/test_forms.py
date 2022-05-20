from django.test import TestCase

from articles.forms import ArticleForm


class TestForms(TestCase):
    def test_valid_article_form(self):
        form = ArticleForm(data={
            'name': 'Test',
            'article': 'Test article',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_article_form(self):
        form = ArticleForm(data={})
        self.assertFalse(form.is_valid())
