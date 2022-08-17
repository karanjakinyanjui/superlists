"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from unittest import skip

from functional_tests.test_functional import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_item(self):
        # Edith goes to the home page and accidentally tries to submit an
        # empty list item. She hits enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # She tries again with some text for the item which now works
        self.fail("Failing ...")
