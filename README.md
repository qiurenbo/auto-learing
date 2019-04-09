# auto-learing
This program is used for auto-learning the video courses in http://zy.jxkp.net. It is only for technology learning.

# 1.For Developers 
## 1.1.Install tesseract
Download the [tesseract for windows x64](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe). 

## 1.2.Download Chrome and relevant driver
1. Download [Chrome 73 driver](https://chromedriver.storage.googleapis.com/73.0.3683.68/chromedriver_win32.zip)

2. Install [Chrome 73](https://www.chrome.com/download/thank-you.html?statcb=1&installdataindex=defaultbrowser)


3. New directory named chrome in the project directory. For example:"D:\Projects\auto-learning\chrome"

4. Copy the all the files under Chrome Application path. For example:C:\Program Files (x86)\Google\Chrome\Application to the "chrome" directory. 

5. Copy the driver to "chrome" directory.

## 1.3.Setup conf.ini
Copy the sample.ini to conf.ini and modify the "Privacy" section.

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
# 2.For users
## 2.1.Download the binary files.
Go to  https://github.com/qiurenbo/auto-learing/releases , Find the latest version download.
## 2.2.Config the conf.ini
replace your username and password

## 2.3.Install tesseract
Install tesseract in the package.

## 2.4.Run the code
Dobule click the auto-learning.exe.
Enjoy yourelf.