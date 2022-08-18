"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django.core.exceptions import ValidationError
from django.db import IntegrityError
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

    def test_duplicate_items_in_list_are_invalid(self):
        item_list = List.objects.create()
        Item.objects.create(text='Item 1', list=item_list)
        with self.assertRaises(IntegrityError):
            item2 = Item(text='Item 1', list=item_list)
            item2.save()

    def test_duplicate_items_in_different_list_are_valid(self):
        item_list = List.objects.create()
        item_list_2 = List.objects.create()
        Item.objects.create(text='Item 1', list=item_list)
        item2 = Item.objects.create(text='Item 1', list=item_list_2)
        item2.full_clean()
        self.assertEqual(Item.objects.count(), 2)

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

    def test_list_ordering(self):
        list1 = List.objects.create()

        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )