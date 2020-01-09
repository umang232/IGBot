from selenium import webdriver
from time import sleep


class InstaFinder:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com/")
        sleep(5)
        self.username = username
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        sleep(2)
        userid = self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        sleep(2)
        passw = self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        sleep(2)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)) \
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]") \
            .click()
        following = self._get_names()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]") \
            .click()
        sleep(2)
        followers = self._get_names()
        print(len(followers))
        print(len(following))

        # People who follow you but you don't follow them back
        list1 = [people for people in followers if people not in following]
        print(list1)
        print(len(list1))

        # People who don't follow you back
        list2 = [people for people in following if people not in followers]
        print(list2)
        print(len(list2))

    def _get_names(self):
        sleep(2)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
            .click()
        return names


InstaFinder(username='your_username', password='your_password')
