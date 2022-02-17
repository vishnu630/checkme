import datetime
import os

from flask import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
year_dic = {
    '11': '2',
    '12': '3',
    '21': '4',
    '22': '5',
    '31': '6',
    '32': '7',
    '41': '8',
    '42': '9'

}
branch_dic = {
    '03': '1',
    '05': '2',
    '04': '3',
    '02': '4',
    '01': '6',
    '12': '10',
    '30': '11'
}

options = Options()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("enable-automation")
# options.add_argument("--disable-infobars")
# options.add_argument("--disable-dev-shm-usage")
web = webdriver.Chrome(executable_path='static/chromedriver', chrome_options=options)
web.implicitly_wait(2)


def login(web):
    user = web.find_element_by_xpath('//*[@id="username"]')
    user.send_keys('jyothsna5')
    passw = web.find_element_by_xpath('//*[@id="password"]')
    passw.send_keys('mayashijo')
    sub = web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[6]/td/input')
    sub.click()


def get_data(adyear, branch, sec1, rollno):
    try:
        web.get('http://202.91.76.90:94/attendance/attendanceTillADate.php')
        year = web.find_element_by_xpath(
            f'/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/select/option[{int(adyear)}]')
        year.click()
        bran = web.find_element_by_xpath(
            f'/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[3]/select/option[{int(branch)}]')
        bran.click()
        sec = web.find_element_by_xpath(
            f'/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[4]/select/option[{sec1}]')
        sec.click()
        show = web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[5]/input[2]')
        show.click()
        att1 = web.find_element_by_xpath(f'//*[@id="{rollno}"]')
        att = att1.text.split('\n')[0][-5:]
        return att
    except:
        pass


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/attshow', methods=['POST', 'GET'])
def attshow():
    if (request.method == 'POST'):
        rollno = request.form['rollno']
        rollno = rollno.upper()
        data = [(rollno[i:i + 2]) for i in range(0, len(rollno), 2)]
        year1 = datetime.datetime.today().year
        month1 = datetime.datetime.today().month
        sem = '1'
        if (data[2] != '1A'):
            data[0] = str(int(data[0]) - 1)
        if (data[0] == '19' or data[0] == '18'):
            if (month1 >= 4):
                sem = '2'
        elif (data[0] == '20' or data[0] == '21'):
            if (month1 >= 5):
                sem = '2'
        year1 = year1 - (2000 + int(data[0]))
        adyear = year_dic[str(year1) + sem]
        branch = branch_dic[data[3]]
        web.get('http://202.91.76.90:94/attendance/attendanceTillADate.php')
        link = web.current_url
        if (link != 'http://202.91.76.90:94/attendance/attendanceTillADate.php'):
            login(web)
        if (data[3] == '12' or data[3] == '30'):
            sec = 1
            att = get_data(adyear, branch, sec, rollno)
        else:
            for i in range(2, 5):
                att = get_data(adyear, branch, i, rollno)
                if(att is None):
                    continue
                else:
                    break
        return render_template('home.html', att=att)

    return 'No Data Found '


if __name__ == '__main__':
    app.run()
