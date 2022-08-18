"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from faker import Faker

fake = Faker()


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        todo_text = fake.sentence()
        self.client.post('/', data={"text": todo_text})
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, todo_text)

    def test_redirects_after_POST(self):
        todo_text = fake.sentence()
        response = self.client.post('/', data={"text": todo_text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_invalid_list_items_are_not_saved(self):
        response = self.client.post('/', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_home_page(self):
        response = self.client.post('/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)