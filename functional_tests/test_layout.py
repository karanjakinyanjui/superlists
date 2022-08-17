"""
Author: Elijah Kinyanjui
(c) Copyright by HugosLabs ltd

File: 
Description: 


"""
from functional_tests.test_functional import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # She notices the input box is nicely centered
        self.assertAlmostEqual(
            self.input_box.location['x'] + self.input_box.size['width'] / 2,
            512,
            delta=10
        )
