
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import os
import logging
import time

from auto_learning import parser
from auto_learning import utils

import requests
from requests.cookies import RequestsCookieJar

class Browser:

    

    def __init__(self, config_file='./conf.ini'):

        self.__driver = webdriver
        self.__options = Options()
        self.__config = parser.ConfigParser(config_file)

        self.__login_url = self.__config.get_setting("DangerZone","login_url")
        self.__login_auth_code_url = self.__config.get_setting("DangerZone","login_auth_code_url")
        self.__username = self.__config.get_setting("Privacy","username")
        self.__password = self.__config.get_setting("Privacy","password")
        self.__auth_code_dir = self.__config.get_setting("DangerZone","auth_code_dir")

        # Set chrome driver options
        self.__options.add_argument('--log-level=WARNING')

        if os.path.exists("./chrome/chrome.exe"):
            self.__options.binary_location = "./chrome/chrome.exe"
        else:
            raise Exception("chrome.exe not fount")

   
        if os.path.exists("./chrome/chromedriver.exe"):
            self.__driver = self.__driver.Chrome(executable_path="./chrome/chromedriver.exe", chrome_options=self.__options)
        else:
            raise Exception("chromedriver.exe not fount")



    def signIn(self):
        self.__driver.get(self.__login_url)
        self.__login_cookies = self.__driver.get_cookies()

        logging.info(self.__login_cookies)
        
        # Automatically fill the input control
        # and try to login
        self.__get_controls()
        self.__fill_controls()
        self.__try_to_login()

        # Try until successful
        while not self.__is_successful():
            self.__fill_controls()
            self.__try_to_login()



    def find_video_urls(self):

        video_table = self.__driver.find_element_by_class_name('table-striped')
        
        # The first row is header, so use [1:-1] to skip
        video_rows = video_table.find_elements_by_tag_name('tr')[1:-1]
        logging.info("Wow, Daddy, I find the viedo info:")

        # logging.info(video_rows)
        video_rows_info = [] 
        for video_row in video_rows:
            video_row_info = [video_column.text for video_column in video_row.find_elements_by_tag_name('td')]
            video_rows_info.append(video_row_info)
       
        logging.info(video_rows_info)


    def __wait_for_element_to_finish(self, elementId, timeout):
        element = self.__driver.find_element_by_id(elementId)
        
        try:
            WebDriverWait(self.__driver, timeout).until(EC.staleness_of(element))
        except exceptions.TimeoutException:
            logging.warn('Daddy, time flys. ')

    def __get_controls(self):
        self.__uInput = self.__driver.find_element_by_name('Uname')
        self.__pInput = self.__driver.find_element_by_name('pass')
        self.__vInput = self.__driver.find_element_by_name('valcode')


    def __fill_controls(self):
        self.__clear_controls()
        self.__set_controls()


    def __clear_controls(self):
        self.__uInput.clear()
        self.__pInput.clear()
        self.__vInput.clear()


    def __set_controls(self):
        auth_code = self.__get_aut_code()

        self.__uInput.send_keys(self.__username)
        self.__pInput.send_keys(self.__password)
        self.__vInput.send_keys(auth_code)

    def __get_absolute_path(self):
        if not os.path.exists(self.__auth_code_dir):
            os.mkdir(self.__auth_code_dir)

        prefix = time.strftime('%Y%m%d%H%M%S', time.localtime())
        return self.__auth_code_dir + '/' + prefix + '_auth_code.png'

    # Use the sessionid in cookie to get the auth code
    def __get_aut_code(self):
        is_recognized = False
        auth_code = ''

        while not is_recognized:
            auth_code_image = requests.get(self.__login_auth_code_url, cookies=self.__get_request_cookies()).content
            image_path = self.__get_absolute_path()

            with open(image_path,'wb') as f:
                f.write(auth_code_image)
                # Ensure the file is written to the disk
                # https://stackoverflow.com/questions/9824806/how-come-a-file-doesnt-get-written-until-i-stop-the-program
                f.flush()
                os.fsync(f.fileno())

            auth_code = utils.ocr(image_path)
            is_recognized = False if auth_code == '' else True

        return auth_code


    def __get_request_cookies(self):
        request_cookies = {}
        for cookie in self.__login_cookies:
            request_cookies[cookie['name']] = cookie['value']

        return request_cookies

    def __try_to_login(self):
        login_btn = self.__driver.find_elements_by_class_name('btn-primary')[1]
        login_btn.click()
        time.sleep(2)
  

    def __is_successful(self):
        try:
            self.__driver.switch_to_alert().accept()
            logging.info('Daddy, I think I made a mistake :(')
            return False
        except exceptions.NoAlertPresentException:
            logging.info('Daddy, I login successfully :)')
            return True
