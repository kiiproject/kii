from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time


class SeleniumTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super(SeleniumTestCase, self).setUp()
        self.keys = Keys
        self.browser = webdriver.Firefox()


    def tearDown(self):
        super(SeleniumTestCase, self).tearDown()
        self.browser.quit()

    def live_login(self, username, password="test"):
        self.browser.get(self.url('kii:user:login'))
        form = self.browser.find_element_by_css_selector("form.login")
        form.find_element_by_css_selector('input[name="username"]').send_keys(username)
        password_input = form.find_element_by_css_selector('input[name="password"]')
        password_input.send_keys(password)
        password_input.send_keys(self.keys.RETURN)

    def url(self, url):
        """Return a full URL from a reversed django url for selenium testing"""
        if not url.startswith('/'):
            # we need reversing 
            url = reverse(url)
        return "{0}{1}".format(self.live_server_url, url)