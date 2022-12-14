"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from selenium import webdriver
from selenium.webdriver.common.by import By

from functional_tests.functional_tests_base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_adding_items(self):
        # Edith has heard about a new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

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

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        to_do_1 = 'Buy peacock feathers'
        self.add_to_do(to_do_1)
        self.check_for_row_in_table(f'1. {to_do_1}')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+/')

        # Now a new user, Francis, comes along to the site
        """
        We use a new browser session to make sure that no information
        of edith is coming through from the cookies etc
        """
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        self.add_to_do('Buy Milk')
        self.check_for_row_in_table('1. Buy Milk')

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+/')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again there is no sign of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
