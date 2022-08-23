from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from functional_tests.functional_tests_base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        """ To set a cookie we need to first visit the domain.
        404 pages load the quickest!
        """
        self.browser.get(self.live_server_url + "/404-not-found")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
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

