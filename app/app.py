import time
import os
from flask import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from waitress import serve
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/attshow',methods=['POST','GET'])
def attshow():
    if(request.method=='POST'):
        rollno=request.form['rollno']
        options = Options()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("enable-automation")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        web = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
        web.implicitly_wait(10)
        web.get('http://202.91.76.90:94/attendance/attendanceTillADate.php')
        try:
            user=web.find_element_by_xpath('//*[@id="username"]')
            user.send_keys('jyothsna5')
            passw=web.find_element_by_xpath('//*[@id="password"]')
            passw.send_keys('mayashijo')
            sub=web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[6]/td/input')
            sub.click()
        except:
            pass
        finally:
            year = web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/select/option[6]')
            year.click()
            bran = web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[3]/select/option[10]')
            bran.click()
            show = web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[5]/input[2]')
            show.click()
            att1 = web.find_element_by_xpath(f'//*[@id="{rollno}"]')
            att= att1.text.split('\n')[0][-5:]
            return render_template('home.html',att=att)
    return 'no'

