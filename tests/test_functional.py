import unittest

import pytest
from selenium import webdriver


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

