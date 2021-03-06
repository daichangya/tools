# Generated by Selenium IDE
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import utils
from db import RedisClient


class TestJianShuPython():
    def setup_method(self):
        self.redis = RedisClient()
        options = webdriver.ChromeOptions()
        # 开发者模式的开关，设置一下，打开浏览器就不会识别为自动化测试工具了
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('user-agent=' + utils.use_ua()["User-Agent"])
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        # options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        proxy = self.redis.random()
        print(proxy)
        options.add_argument('--proxy-server=http://' + proxy)
        self.driver = webdriver.Chrome('/home/daichangya/文档/chromedriver', chrome_options=options)
        self.driver.implicitly_wait(20)  # 隐性等待，最长等20秒
        self.driver_is_ok = True
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(25)
        self.driver.set_script_timeout(25)  # 这两种设置都进行才有效
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))

    def test_testPython(self):
        try:
            self.driver.get("https://www.jianshu.com/c/24f898ba81ca")
            self.driver.set_window_size(1936, 1056)
            self.read_artcile()
            page_height = self.driver.execute_script('return document.documentElement.scrollHeight;')
            print(page_height)
            titleList = ["（Python基础教程之十七）Python OrderedDict –有序字典"]
            for title in titleList:
                self.driver.execute_script("window.scrollTo(0,100)")
                windowLength = 500
                while True:
                    print(title)
                    elements = self.driver.find_elements(By.LINK_TEXT, title)
                    if (len(elements) > 0):
                        self.driver.find_element(By.LINK_TEXT, title).click()
                        break
                    else:
                        windowLength = windowLength + 500
                        if windowLength>page_height:
                            break
                        javaScript = "window.scrollTo(0,{})".format(windowLength)
                        print(javaScript)
                        self.driver.execute_script(javaScript)
            self.read_artcile()
            self.driver.close()
        except Exception as e:
            print(e)
            self.driver.quit()


    def read_artcile(self):
        timeGG = 10000
        windowLength = 500
        page_height = self.driver.execute_script('return document.documentElement.scrollHeight;')
        print(page_height)
        while True:
            self.wait_for_window(timeGG)
            windowLength = windowLength + random.randint(300, 1000)
            javaScript = "window.scrollTo(0,{})".format(windowLength)
            print(javaScript)
            self.driver.execute_script(javaScript)
            if windowLength > page_height - 300:
                break
        # self.driver.execute_script("window.scrollTo(0,600)")


if __name__ == '__main__':
    test = TestJianShuPython()
    for i in range(20):
        test.setup_method()
        test.test_testPython()
        test.teardown_method()
        time.sleep(round(10000 / 1000))
