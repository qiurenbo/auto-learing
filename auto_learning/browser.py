
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
import os
import logging
import urllib.request
from auto_learning import parser


class Browser:



    def __init__(self, config_file='./conf.ini'):

        self.__driver = webdriver
        self.__options = Options()
        self.__config = parser.ConfigParser(config_file)

        self.__login_url = self.__config.get_setting("DangerZone","login_url")
        self.__login_auth_code_url = self.__config.get_setting("DangerZone","login_auth_code_url")
        self.__username = self.__config.get_setting("Privacy","username")
        self.__password = self.__config.get_setting("Privacy","password")

        ### Set chrome driver options
        self.__options.add_argument('--log-level=OFF')

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

        unameInput = self.__driver.find_element_by_name('Uname')
        passInput = self.__driver.find_element_by_name('pass')
        
        logging.info('sign in, Daddy')

        unameInput.send_keys(self.__username)
        passInput.send_keys(self.__password)

        # imgElement = driver.find_element_by_id('codeImg')
        # authCodeText = self.get_auth_code(driver,imgElement)


        urllib.request.urlretrieve(self.__login_auth_code_url, "validat.png")
        # Wait for user to sign in
        self.wait_for_element_to_finish("login_form", 270)
        
        logging.info('sign in, Daddy')


    def wait_for_element_to_finish(self, elementId, timeout):
        signIn = self.__driver.find_element_by_id(elementId)
        
        try:
            WebDriverWait(self.__driver, timeout).until(EC.staleness_of(signIn))
        except exceptions.TimeoutException:
            logging.warn('Daddy, are you asleep? :( ')


    # def get_auth_code(self,codeEelement):
    #     self.__driver.save_screenshot('login/login.png')  #截取登录页面
    #     imgSize = codeEelement.size   #获取验证码图片的大小
    #     imgLocation = codeEelement.location #获取验证码元素坐标
    #     rangle = (int(imgLocation['x']),int(imgLocation['y']),int(imgLocation['x'] + imgSize['width']),int(imgLocation['y']+imgSize['height']))  #计算验证码整体坐标
    #     login = Image.open("login/login.png")  
    #     frame4=login.crop(rangle)   #截取验证码图片
    #     frame4.save('login/authcode.png')

    #     return authCodeText