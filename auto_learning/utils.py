import PIL
import pytesseract
import logging

def ocr(image_path):

    logging.info('Daddy, I find image_path is:{}'.format(image_path))

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    image = PIL.Image.open(image_path)

    text = pytesseract.image_to_string(image)

    if text == '':
        logging.info('Daddy, It is too hard for tesseract :(')
    else:
        logging.info('Daddy, I know these words:{}'.format(text))

    return text