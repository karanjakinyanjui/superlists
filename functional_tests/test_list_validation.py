"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""

from functional_tests.functional_tests_base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR


class ListValidationTest(FunctionalTest):
    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.add_to_do('Buy Wellies')
        self.check_for_row_in_table('1. Buy Wellies')

        # She accidentally tries to enter a duplicate item
        self.add_to_do('Buy Wellies')

        # She sees a helpful error message
        self.wait_for_error_message(DUPLICATE_ITEM_ERROR)