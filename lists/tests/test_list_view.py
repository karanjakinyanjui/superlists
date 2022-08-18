"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from django.test import TestCase
from django.utils.html import escape

from lists.models import List, Item


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

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_invalid_list_items_are_not_saved(self):
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/', data={'text': 'First Item'})
        self.client.post(f'/lists/{correct_list.id}/', data={'text': ''})
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
