"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
import re
from time import sleep

import pytest
from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.test_functional import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.email_input_box.send_keys(TEST_EMAIL)

        self.email_input_box.send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        # She checks her mail and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        self.assertTrue(url_search, f"Could not find url in email body:\n {email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks on the log in link
        self.browser.get(url)

        # She is logged in
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Log Out')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        logout_btn = self.browser.find_element(By.LINK_TEXT, 'Log Out')
        logout_btn.click()

        self.wait_for(
            lambda: self.browser.find_element(By.NAME, 'email')
        )
