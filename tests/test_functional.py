import time
import unittest

import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    @pytest.mark.e2e
    def test_django_app(self):
        # Edith has heard about a new online to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8080')

        # She notices the page title and header mentions to-do lists
        assert 'To-Do' in self.browser.title, f"Browser title was `{self.browser.title}`"

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element('#new_item_input')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item',
                         "Input box placeholder not correct")

        # She types "Buy Peacock feathers" into a text box
        input_box.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page list
        # "1. Buy peacock feathers"
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'to-do-list-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(rows[1].text, '1. Buy peacock feathers')
