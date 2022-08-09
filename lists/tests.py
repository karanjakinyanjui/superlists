from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
        html = response.content.decode('utf-8').strip()
        self.assertIn('<title>To-Do lists</title>', html)

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={"text": "A new list item"})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')
