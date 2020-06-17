def test_student_login(self):
        driver = self.driver
        print("Driver initiated successfully.  Navigate url")
        driver.get("https://uwiciitonline.azurewebsites.net")
    
        print("loading uwiciit platform with invalid credentials ")
        time.sleep(8)
        elem = driver.find_element_by_id("username")
        elem.send_keys("413002757")
        elem = driver.find_element_by_id("password")
        elem.send_keys("tester2")
        elem.submit()
        print("Printing title of current page :"+driver.title)
        driver.execute_script("lambda-status=failed")
        print("Requesting to mark test : failed")

        print("loading uwiciit platform with valid credentials ")
        time.sleep(8)
        elem = driver.find_element_by_id("username")
        elem.send_keys("413002757")
        elem = driver.find_element_by_id("password")
        elem.send_keys("tester")
        elem.submit()
 
        print("Printing title of current page :"+driver.title)
        driver.execute_script("lambda-status=passed")
        print("Requesting to mark test : pass")
    
    
    def test_admin_login(self):
        driver = self.driver
        print("Driver initiated successfully.  Navigate url")
        driver.get("https://uwiciitonline.azurewebsites.net")
    
        print("loading uwiciit admin platform with invalid credentials ")
        time.sleep(8)
        elem = driver.find_element_by_id("username")
        elem.send_keys("412002010")
        elem = driver.find_element_by_id("password")
        elem.send_keys("badcredentials")
        elem.submit()
        print("Printing title of current page :"+driver.title)
        driver.execute_script("lambda-status=failed")
        print("Requesting to mark test : failed")

        print("loading uwiciit platform with valid credentials ")
        time.sleep(8)
        elem = driver.find_element_by_id("username")
        elem.send_keys("412002010")
        elem = driver.find_element_by_id("password")
        elem.send_keys("passWord")
        elem.submit()
 
        print("Printing title of current page :"+driver.title)
        driver.execute_script("lambda-status=passed")
        print("Requesting to mark test : pass")