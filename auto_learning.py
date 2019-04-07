from auto_learning import browser
import logging


if __name__ == '__main__':

    logging_format = '%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s  %(message)s'
    logging.basicConfig(level=logging.INFO, format=logging_format)
    browser = browser.Browser()
    browser.signIn()
    browser.find_video_urls()