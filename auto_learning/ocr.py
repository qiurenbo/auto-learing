import PIL
import pytesseract

def ocr():
    auth_code_img = PIL.Image.open('./auth_code.png')
    text = pytesseract.image_to_string(auth_code_img).strip()
    print(text)