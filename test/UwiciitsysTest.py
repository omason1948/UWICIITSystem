import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
 
class LTAutomate(unittest.TestCase):
    
    def setUp(self):
        # username: Username can be found at automation dashboard
        username=" " 
        # accessToken:  AccessToken can be generated from automation dashboard or profile section
        accessToken=" "
        # gridUrl: gridUrl can be found at automation dashboard
        gridUrl = "hub.lambdatest.com/wd/hub"
         
        desired_cap = {
            'platform' : "win10",
            'browserName' : "chrome",
            'version' :  "67.0",
            # Resolution of machine
            "resolution": "1024x768",
            "name": "UWICIIT System test ",
            "build": "UWICIIT System build",
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
    def test_search_in_google(self):
        driver = self.driver
        print("Success!")
        driver.get("https://uwiciitonline.azurewebsites.net")
    
        print("Testing UWICIIT System ")
        userlogin = driver.find_element_by_name("username")
        userlogin.send_keys("415002479")
        userpassword = driver.find_element_by_name("password")
        userpassword.send_keys("Password7")
        login = driver.find_element_by_name("submit")
        login.click()

        studentInfo = driver.find_element_by_id("menuItem-studentInfo")
        studentInfo.click()

        personalDetails = driver.find_element_by_id("personalDetails")
        personalDetails.click()

        updateDetail = driver.find_element_by_id("updateInfo")
        updateDetail.click()

        cancelButton = driver.find_element_by_id("cancel")
        cancelButton.click()     

        personalinfo = driver.find_element_by_id("personalInfoHeader")
        personalinfo.click()

        query = driver.find_element_by_id("studentQuery")
        query.click()

        year = Select(driver.find_element_by_id("yearOfStudy"))
        year.select_by_visible_text("Year 3")

        semester = Select(driver.find_element_by_id("semester"))
        semester.select_by_visible_text("Summer")

        issue = Select(driver.find_element_by_id("studentIssues"))
        issue.select_by_visible_text("Finance")

        description = driver.find_element_by_id("queryDesc")
        description.send_keys("I am seeing descrepancies in my fiances please investigate.")
    
        submit = driver.find_element_by_id("submitbtn")
        submit.click()

        confirmsubmit = driver.find_element_by_name("submit")
        confirmsubmit.click()
        
        print("Printing title of current page :"+driver.title)
        driver.execute_script("lambda-status=passed")
        print("Requesting to mark test : pass")

if __name__ == "__main__":
    unittest.main()
