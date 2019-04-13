from autolearn import browser, utils
import logging

if __name__ == '__main__':

    #logging_format = '%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s  %(message)s'
    # Config the logging

    utils.mkdir_if_not_exists('log')
    logging_format = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.INFO, format=logging_format)
    logger = logging.getLogger()
    fh = logging.FileHandler('./log/log_'+utils.get_nowtime()+'.txt')
    logger.addHandler(fh)


    # Self studying
    browser = browser.Browser()
    browser.signin()
    browser.study()
    browser.quit()

