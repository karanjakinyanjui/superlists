from django.test import TestCase
from django.urls import resolve
from faker import Faker

from lists.views import home_page
from lists.models import Item

fake = Faker()


class ItemModelTest(TestCase):
    def test_add_items(self):
        first_item = Item.objects.create(text='The first list item')
        self.assertEqual(Item.objects.count(), 1)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_displays_all_items(self):
        first_item = Item.objects.create(text='The first list item')
        second_item = Item.objects.create(text='The second list item')

        response = self.client.get('/')

        self.assertIn('The first list item', response.content.decode())
        self.assertIn('The second list item', response.content.decode())

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
        html = response.content.decode('utf-8').strip()
        self.assertIn('<title>To-Do lists</title>', html)

    def test_can_save_a_POST_request(self):
        todo_text = fake.sentence()
        self.client.post('/', data={"text": todo_text})
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, todo_text)

    def test_redirects_after_POST_request(self):
        todo_text = fake.sentence()
        response = self.client.post('/', data={"text": todo_text})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
