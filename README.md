# auto-learing
This program is used for auto-learning the video courses in http://zy.jxkp.net. It is only for technology learning.

# 1.How to use this code 
## 1.1.Install tesseract
Download the tesseract for windows x64.

https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe

## 1.2.Download Chrome and relevant driver
Download driver 73:
https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_win32.zip

Install Chrome73:
https://www.chrome.com/download/thank-you.html?statcb=1&installdataindex=defaultbrowser

Make chrome directory in the project directory like D:\Projects\auto-learning\chrome

Copy the all the files under Chrome Application path like C:\Program Files (x86)\Google\Chrome\Application to the chrome directory. 

Copy the driver to chrome directory.

## 1.3.Setup conf.ini
Copy the sample.ini to conf.ini and modify the 'Privacy' section.

## 1.4.Run the code in virtualenv
```
cd auto_learning
```
```
pip install -r requirements.txt
```
```
python auto_learning.py
```

## Enjoy yourelf.