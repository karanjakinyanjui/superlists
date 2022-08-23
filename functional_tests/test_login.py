"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.functional_tests_base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.email_input_box.send_keys(self.test_email)

        self.email_input_box.send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for_login_email_sent_message()

        # She checks her mail and finds a message
        email = self.wait_for_email(self.test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        self.assertTrue(url_search, f"Could not find url in email body:\n {email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks on the log in link
        self.browser.get(url)

        # She is logged in
        self.wait_to_be_logged_in(self.test_email)

        # She clicks on the logout button
        self.logout_btn.click()

        # She is logged out
        self.wait_to_be_logged_out(self.test_email)

    def wait_for_email(self, email_address, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(email_address, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(email_address)
            inbox.pass_(os.environ['EMAIL_PASSWORD'])
            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print(f'getting msg {i}')
                    _, lines, __ = inbox.retr(i)
                    lines = [line.decode('utf8') for line in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
