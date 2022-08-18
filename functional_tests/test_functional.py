import os
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

MAX_WAIT = 10


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f"http://{staging_server}"

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def wait_for(self, fn):
        start = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def check_for_row_in_table(self, row_text):
        def check_for_row(text):
            table = self.browser.find_element(By.ID, 'to-do-list-table')
            rows = table.find_elements(By.TAG_NAME, 'tr')
            self.assertIn(text, [row.text for row in rows])
        self.wait_for(lambda: check_for_row(row_text))

    def add_to_do(self, text):
        self.input_box.send_keys(text)
        self.input_box.send_keys(Keys.ENTER)

    # def add_to_do_and_check(self, text):

    @property
    def input_box(self):
        return self.browser.find_element(By.ID, 'new_item_input')

