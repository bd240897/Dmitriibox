from multiprocessing import Process
from django.test import TestCase
from selenium import selenium

class SeleniumFixtureCase(TestCase):
    """
    Wrapper to multiprocess localhost server and selenium instance on one
    test run.
    """

    def setUp(self):
        "Make the selenium connection"
        TestCase.setUp(self)
        self.server = Process(target=serve)
        self.server.start()
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox",
                                 "http://localhost:8000/")
        self.selenium.start()

    def tearDown(self):
        "Kill processes"
        TestCase.tearDown(self)
        self.server.terminate()
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

    def _login(self):
        "Login as Albert Camus"
        self.selenium.open("http://localhost:8000/admin/")
        self.selenium.wait_for_page_to_load("30000")
        self.selenium.type("id_username", "albert")
        self.selenium.type("id_password", "albert")
        self.selenium.click("//input[@value='Log in']")
        self.selenium.wait_for_page_to_load("30000")