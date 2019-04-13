
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import os
import logging
import time

from autolearn import config_parser, utils

import requests
from requests.cookies import RequestsCookieJar

class Browser:

    

    def __init__(self):

        self.__driver = webdriver
        self.__options = Options()
        self.__config = config_parser.ConfigParser()

        self.__login_url = self.__config.get_setting("DangerZone","login_url")
        self.__login_auth_code_url = self.__config.get_setting("DangerZone","login_auth_code_url")
        self.__auth_code_dir = self.__config.get_setting("DangerZone","auth_code_dir")

        self.__username = self.__config.get_setting("Privacy","username")
        self.__password = self.__config.get_setting("Privacy","password")

        # Set chrome driver options
        self.__options.add_argument('--log-level=WARNING')
        self.__options.add_argument('--mute-audio')

        if self.__config.get_setting("DangerZone","headless") == 'True':
            self.__options.add_argument('--headless')

        if os.path.exists("./chrome/chrome.exe"):
            self.__options.binary_location = "./chrome/chrome.exe"
        else:
            raise Exception("chrome.exe not fount")

   
        if os.path.exists("./chrome/chromedriver.exe"):
            self.__driver = self.__driver.Chrome(executable_path="./chrome/chromedriver.exe", chrome_options=self.__options)
        else:
            raise Exception("chromedriver.exe not fount")



    def signin(self):
        self.__driver.get(self.__login_url)
        self.__login_cookies = self.__driver.get_cookies()

        logging.info(self.__login_cookies)
        
        # Automatically fill the input control
        # and try to login
        self.__get_controls()
        is_successful = False

        # Try until successful
        while not is_successful:
            self.__fill_controls()
            self.__try_to_login()
            is_successful = self.__is_successful()


    def study(self):

        is_courses_over = False
        while not is_courses_over:
            # If refresh the page, we must re-get the dom elements
            unfinished_courses = self.__get_unfinished_courses()
            
            if unfinished_courses:
                self.__choose_course(unfinished_courses[0])
                
                is_lessons_over = False
                while not is_lessons_over:
                    unfinished_lessons = self.__get_unfinished_lessons()
                    
                    if unfinished_lessons:
                        self.__choose_lesson(unfinished_lessons[0])
                        self.__super_player()

                        # If finish the lesson, go back to the lessons list
                        self.__driver.execute_script("window.history.go(-1)")
                        self.__driver.refresh()
                        time.sleep(3)

                    # If there are no unfinished lessons,
                    # go back to courses list
                    else:
                        is_lessons_over = True
                        self.__driver.execute_script("window.history.go(-1)")
                        self.__driver.refresh()
                        time.sleep(3)

            # If there are no unfinished courses,
            # finsh auto-learning
            else:
                is_courses_over = True

    def quit(self):
        if (self.__driver):
            self.__driver.quit()
    
    def __get_unfinished_courses(self):
        courses = self.__find_interesting_table()
        return [course for course in courses if course[-2] == '未完成' ]


    def __get_unfinished_lessons(self):
        lessons = self.__find_interesting_table()
        return [lesson for lesson in lessons if lesson[-2] == '未完成']

    def __choose_course(self, unfinished_course):
        unfinished_course[-1].click()
        logging.info('OK, I clicked the course:{}'.format(unfinished_course[0]))
        logging.info(unfinished_course)


    def __choose_lesson(self, unfinished_lesson):
        unfinished_lesson[-1].click()
        logging.info('OK, I clicked the lesson:{}'.format(unfinished_lesson[0]))
        logging.info(unfinished_lesson)

    def __super_player(self):
        logging.info('Wow, play the viedo incrediblely')

        # Get video duration
        video_duration_element = self.__driver.find_element_by_class_name("vjs-duration-display")
        # The duration is on DOM tree when the page loaded, so it is unnecessary to move the mouse.
        # action = ActionChains(self.__driver)
        # action.move_to_element(video_duration_element).perform()
        WebDriverWait(self.__driver, 180, 0.2).until(EC.visibility_of(video_duration_element))
        
        minutes, seconds = video_duration_element.text.replace('Duration Time','').split(':')
        learning_time = int(minutes) * 60 + int(seconds) + 10
        logging.info("video duration {} seconds".format(learning_time))

        already_learning_time = 0

        # Remove blur\focus listener
        self.__driver.execute_script('$(window).off(\'blur focus\');')
        while learning_time > 0:
            learning_time = learning_time - 1
            already_learning_time = already_learning_time + 1
            time.sleep(1)
            if already_learning_time % 60 == 0:
                logging.info("I have already learned {} minutes, {} minutes remaining".format(already_learning_time / 60, learning_time / 60))


    def __find_interesting_table(self):
        interesting_table = self.__driver.find_element_by_class_name('table-striped')
        
        # The first row is header, so use [1:] to skip it
        interesting_rows = interesting_table.find_elements_by_tag_name('tr')[1:]

        interestings = [] 
        for interesting_row in interesting_rows:
            interesting_columns = interesting_row.find_elements_by_tag_name('td')
            interesting = [interesting_column.text for interesting_column in interesting_columns]

            # Append hyperlink element
            interesting.append(interesting_columns[0].find_element_by_tag_name('a'))
            interestings.append(interesting)
        logging.info(interestings)
        return interestings

    def __wait_for_element_to_finish(self, elementId, timeout):
        element = self.__driver.find_element_by_id(elementId)
        
        try:
            WebDriverWait(self.__driver, timeout).until(EC.staleness_of(element))
        except exceptions.TimeoutException:
            logging.warn('Daddy, time flys.')

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
        utils.mkdir_if_not_exists(self.__auth_code_dir)
        prefix = utils.get_nowtime()
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
