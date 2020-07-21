
"""

Execute Python Automation Tests on LambdaTest Distributed Selenium Grid
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import datetime
from datetime import datetime
 
class LTAutomate(unittest.TestCase):
 
    """
    Setup remote driver
    Params
    ----------
    platform : Supported platform - (Windows 10, Windows 8.1, Windows 8, Windows 7,  macOS High Sierra, macOS Sierra, OS X El Capitan, OS X Yosemite, OS X Mavericks)
    browserName : Supported platform - (chrome, firefox, Internet Explorer, MicrosoftEdge)
    version :  Supported list of version can be found at https://www.lambdatest.com/capabilities-generator/
 
    Result
    -------
    """
    def setUp(self):
        # username: Username can be found at automation dashboard
        username="2661998" 
        # accessToken:  AccessToken can be generated from automation dashboard or profile section
        accessToken="UtIy6LEgxVQ24t2o6GwcArLwrOAxLlq4ycA2KE2YZamlHcyyJC"
        # gridUrl: gridUrl can be found at automation dashboard
        gridUrl = "hub.lambdatest.com/wd/hub"
         
        desired_cap = {
            'platform' : "win10",
            'browserName' : "chrome",
            'version' :  "67.0",
            # Resolution of machine
            "resolution": "1024x768",
            "name": "LambdaTest python google search test ",
            "build": "LambdaTest python google search build",
            "network": True,
            "video": True,
            "visual": True,
            "console": True,
        }
 
        # URL: https://{username}:{accessToken}@hub.lambdatest.com/wd/hub
        url = "https://"+username+":"+accessToken+"@"+gridUrl
         
        print("Initiating remote driver on platform: "+desired_cap["platform"]+" browser: "+desired_cap["browserName"]+" version: "+desired_cap["version"])
        self.driver = webdriver.Remote(
            desired_capabilities=desired_cap,
            command_executor= url
        )
 
    """
    Setup remote driver
    Params
    ----------
    Execute test:  navigate google.com search LambdaTest
    Result
    -------
    print title
    """
    def test_delete(self):
        driver = self.driver
        print("Driver initiated successfully.Navigating to url")
        driver.get("https://uwiciitonline.azurewebsites.net/login")
 
        print("Logging in on the UWICIIT System. ")
        time.sleep(8)

        elem = driver.find_element_by_name("username")
        elem.send_keys("12345")
        essem = driver.find_element_by_name("password")
        essem.send_keys("Something")
        login = driver.find_element_by_name("submit")
        login.click()

        header = driver.find_element_by_id("eventHeader")
        header.click()

        delete = driver.find_element_by_css_selector("a[href='/events/delete/5eea6de5599b1f2fbcd7e132']")
        delete.click()

        
        findtext = driver.find_elements_by_xpath("//*[contains(text(), 'The event has been deleted.')]")

        if not findtext:
            print("No element found.")
        else:
            print("Printing title of current page :"+driver.title)
            driver.execute_script("lambda-status=passed")
            print("Requesting to mark test : pass")
        
        

 
    """
    Quit selenium driver
    """
    def tearDown(self):
        self.driver.quit()
 
if __name__ == "__main__":
    unittest.main()