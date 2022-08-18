"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""

from django.test import TestCase
from faker import Faker

from lists.models import List, Item

fake = Faker()


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        todo_text = fake.sentence()
        self.client.post(
            f'/lists/{correct_list.id}/',
            data={"text": todo_text}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, todo_text)
        self.assertEqual(new_item.list, correct_list)

    def test_invalid_list_items_are_not_saved(self):
        item_list = List.objects.create()

        self.client.post(f'/lists/{item_list.id}/', data={'text': 'First Item'})
        self.client.post(f'/lists/{item_list.id}/add_item', data={'text': ''})
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
