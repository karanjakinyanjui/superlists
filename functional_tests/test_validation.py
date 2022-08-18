"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from unittest import skip

from selenium.webdriver.common.by import By

from functional_tests.test_functional import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Edith goes to the home page and accidentally tries to submit an
        # empty list item. She hits enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.browser.get(self.live_server_url)
        self.add_to_do("")
        self.wait_for(lambda:
            self.assertEqual(
                self.browser.find_element(By.CLASS_NAME, "has-error").text,
                "You can't have an empty list item"
            )
        )
        # She tries again with some text for the item which now works
        self.add_to_do("Buy Milk")
        self.check_for_row_in_table("1. Buy Milk")

        # She tries to submit an empty list on the lists page

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.add_to_do("")

        self.wait_for(lambda:
            self.assertEqual(
                self.browser.find_element(By.CLASS_NAME, "has-error").text,
                "You can't have an empty list item"
            )
        )

        # She tries again with some text for the item which now works
        self.add_to_do("Buy Bread")
        self.check_for_row_in_table("2. Buy Bread")

        # self.fail("Failing ...")
