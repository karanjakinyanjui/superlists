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

    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element(By.ID, 'to-do-list-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, (row.text for row in rows))

    @pytest.mark.e2e
    def test_django_app(self):
        # Edith has heard about a new online to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8080')

        # She notices the page title and header mentions to-do lists
        assert 'To-Do' in self.browser.title, f"Browser title was `{self.browser.title}`"
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        self.assertEqual(self.input_box.get_attribute('placeholder'), 'Enter a to-do item',
                         "Input box placeholder not correct")

        # She types "Buy Peacock feathers" into a text box and hits enter
        to_do_1 = 'Buy peacock feathers'
        self.add_to_do(to_do_1)

        # the page updates, and now the page list
        # Should show the newly added to-do
        self.check_for_row_in_table(f'1. {to_do_1}')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        to_do_2 = 'Use peacock feathers to make a fly'
        self.add_to_do(to_do_2)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_table(f'2. {to_do_2}')

    def add_to_do(self, text):
        self.input_box.send_keys(text)
        self.input_box.send_keys(Keys.ENTER)
        time.sleep(2)

    @property
    def input_box(self):
        return self.browser.find_element(By.ID, 'new_item_input')
