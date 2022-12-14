from django.conf import settings
from django.contrib.auth import get_user_model


from functional_tests.functional_tests_base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_authenticated_session
from functional_tests.server_tools import create_session_on_server
User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        """ To set a cookie we need to first visit the domain.
        404 pages load the quickest!
        """
        self.browser.get(self.live_server_url + "/404-not-found")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

