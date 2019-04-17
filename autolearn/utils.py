import PIL
import pytesseract
import logging
import time
import os
import configparser

class ConfigParser:

    config = configparser.ConfigParser()

    def __init__(self, config_file = './conf.ini'):
        self.config.read(config_file)

    def get_setting(self, section, property):
        return self.config[section][property]



class Tesseract():

    def __init__(self):
        self.__tesseract = pytesseract.pytesseract
        self.__tesseract.tesseract_cmd = ConfigParser().get_setting("DangerZone","tesseract_cmd_path")
    
    def ocr(self, image_path):

        logging.info('Daddy, I find the image path is:{}'.format(image_path))

        image = PIL.Image.open(image_path)

        text = self.__tesseract.image_to_string(image)

        if text == '':
            logging.info('Daddy, It is too hard for tesseract :(')
        else:
            logging.info('Daddy, I know these words:{}'.format(text))

        return text


def get_nowtime():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())



def mkdir_if_not_exists(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)