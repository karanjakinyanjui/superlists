from django.test import TestCase
from django.urls import resolve
from faker import Faker

from lists.views import home_page
from lists.models import Item, List

fake = Faker()


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item_list = List.objects.create()

        Item.objects.create(text='The first list item', list=item_list)
        Item.objects.create(text='The second list item', list=item_list)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, item_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'The first list item')
        self.assertEqual(saved_items[1].text, 'The second list item')
        self.assertEqual(saved_items[0].list, item_list)
        self.assertEqual(saved_items[1].list, item_list)


class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()

        Item.objects.create(text='The first list item', list=correct_list)
        Item.objects.create(text='The second list item', list=correct_list)

        other_list = List.objects.create()

        Item.objects.create(text='Other list item 1', list=other_list)
        Item.objects.create(text='Other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'The first list item')
        self.assertContains(response, 'The second list item')

        self.assertNotContains(response, 'Other list item 1')
        self.assertNotContains(response, 'Other list item 2')

    def test_uses_list_template(self):
        item_list = List.objects.create()

        response = self.client.get(f'/lists/{item_list.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        todo_text = fake.sentence()
        self.client.post('/lists/new', data={"text": todo_text})
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, todo_text)

    def test_redirects_after_POST(self):
        todo_text = fake.sentence()
        response = self.client.post('/lists/new', data={"text": todo_text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')
        html = response.content.decode('utf-8').strip()
        self.assertIn('<title>To-Do lists</title>', html)
