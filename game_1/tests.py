from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # options
        options = webdriver.ChromeOptions()
        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        # for ChromeDriver version 79.0.3945.16 or over
        options.add_argument("--disable-blink-features=AutomationControlled")
        # path to driver
        path_driver = "C:\Games\Python_works\Dmitriibox\chromedriver\chromedriver.exe"
        service = Service(path_driver)
        driver = webdriver.Chrome(
            service=service,
            options=options
        )
        cls.selenium = webdriver.Chrome(service=service, options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.close()
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        # (3)
        # логин
        input_username = self.selenium.find_element(By.CSS_SELECTOR, "#id_username")
        input_username.clear()
        input_username.send_keys('user1')

        input_password = self.selenium.find_element(By.CSS_SELECTOR, "#id_password")
        input_password.clear()
        input_password.send_keys('1234qwerS')

        btn_submit = self.selenium.find_element(By.CSS_SELECTOR, "[type='submit']")
        btn_submit.click()
        time.sleep(1)
