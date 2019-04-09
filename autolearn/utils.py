import PIL
import pytesseract
import logging
from autolearn import config_parser
import time
import os

pytesseract.pytesseract.tesseract_cmd = config_parser.ConfigParser().get_setting("DangerZone","tesseract_cmd_path")

def ocr(image_path):

    logging.info('Daddy, I find the image path is:{}'.format(image_path))

    image = PIL.Image.open(image_path)

    text = pytesseract.image_to_string(image)

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