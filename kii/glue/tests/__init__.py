from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class SeleniumTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super(SeleniumTestCase, self).setUp()
        self.keys = Keys
        self.browser = webdriver.Firefox()


    def tearDown(self):
        super(SeleniumTestCase, self).tearDown()
        self.browser.quit()

    def url(self, url):
        """Return a full URL from a reversed django url for selenium testing"""
        if not url.startswith('/'):
            # we need reversing 
            url = reverse(url)
        return "{0}{1}".format(self.live_server_url, url)