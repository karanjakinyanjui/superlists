import unittest
from selenium import webdriver



class FunctionalTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8080')

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def test_django_app(self):
        assert 'success' in self.browser.title

