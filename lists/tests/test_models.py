"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import List, Item


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

    def test_cannot_save_empty_list_items(self):
        item_list = List.objects.create()
        item = Item.objects.create(text='', list=item_list)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')