from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django_dynamic_fixture import G
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


class GlueTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):

        self.browser.quit()

    def url(self, url):
        """Return a full URL from a reversed django url for selenium testing"""
        return "{0}{1}".format(self.live_server_url, url)

    def test_user_can_display_home_page_and_login(self):

        # Harold is a regular Kii user
        user = G(get_user_model(), username="harold")
        user.set_password('test')
        user.save()

        # As every morning, he opens Kii's homepage
        # withing his web browser
        self.browser.get(self.url(reverse('kii:glue:home')))

        # He sees a welcome message
        self.assertIn('Welcome', self.browser.title)

        # And, below, a login form
        login_form = self.browser.find_element_by_css_selector("form#login")
        username_input = login_form.find_element_by_css_selector('input[type="text"]')
        password_input = login_form.find_element_by_css_selector('input[name="password"]')

        # He fills the form
        username_input.send_keys('harold')
        password_input.send_keys('test')
        password_input.send_keys(Keys.RETURN)

        # He is redirected to his homepage and a popup notice him he has successfully
        # logged in
        result_popup = self.browser.find_element_by_css_selector(".messages .success")
        self.assertIn('user.login.success', result_popup.text)

        # his homepage lists currently enabled apps
        apps = self.browser.find_elements_by_css_selector(".apps > li > a")
        expected_apps = app_manager.filter(user_access=True)
        self.assertEqual(len(apps), len(expected_apps))
        for i, app in enumerate(apps)
            self.assertEqual(app.text, expected_apps[i].verbose_name)