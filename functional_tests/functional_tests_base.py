import os
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f"http://{staging_server}"

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    @wait
    def check_for_row_in_table(self, row_text):
        table = self.browser.find_element(By.ID, 'to-do-list-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def add_to_do(self, text):
        self.input_box.send_keys(text)
        self.input_box.send_keys(Keys.ENTER)

    # def add_to_do_and_check(self, text):

    @property
    def input_box(self):
        return self.browser.find_element(By.ID, 'new_item_input')

    @property
    def email_input_box(self):
        return self.browser.find_element(By.NAME, 'email')

    @property
    def logout_btn(self):
        return self.browser.find_element(By.LINK_TEXT, 'Log Out')

    @property
    def navbar(self):
        return self.browser.find_element(By.CSS_SELECTOR, '.navbar')

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.NAME, 'email')
        self.assertNotIn(email, self.navbar.text)

    @wait
    def wait_to_be_logged_in(self, email):
        self.assertIn(email, self.navbar.text)

    @wait
    def wait_for_error_message(self, error):
        self.assertIn(error, self.browser.find_element(By.CLASS_NAME, 'has-error').text)

    @wait
    def wait_for_login_email_sent_message(self):
        self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    @wait
    def wait_for_invalid_input_message(self):
        return self.browser.find_element(By.CSS_SELECTOR, "#new_item_input:invalid")
