import datetime
import os
from flask import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = 'thisismysiteforattendance12121@#2143432543645732432@!@42mlkdnvkjdsnvdsdskjbgkjdsb'
fdata = []
sdata = []
tdata = []
frdata = []
cache_data = dict()
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


@app.errorhandler(404)
def handle_404(e):
    return redirect('/')


@app.errorhandler(500)
def handle_500(e):
    flash("Check Your RollNO Number")
    return redirect('/')


@app.route('/')
def index():
    return redirect('/home/')


@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/ThankU/')
def thank_you():
    return render_template('thank_you.html')


options = Options()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
web = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
web.implicitly_wait(1)


def login(web):
    user = web.find_element_by_xpath('//*[@id="username"]')
    user.send_keys('jyothsna5')
    passw = web.find_element_by_xpath('//*[@id="password"]')
    passw.send_keys('mayashijo')
    sub = web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[6]/td/input')
    sub.click()


def get_data(adyear, branch, sec1, rollno):
    try:
        get_data.sec1 = sec1
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
        if att == rollno[5::]:
            att = att1.text.split('\n')[1][-5:]
        return att
    except:
        pass


@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/attshow', methods=['POST', 'GET'])
def attshow():
    global att
    if request.method == 'POST':
        rollno = request.form['rollno']
        rollno = rollno.upper()
        if not (len(rollno) == 10 and 'KB' in rollno and '1A' in rollno or '5A' in rollno):
            flash("Check Your RollNO Number")
            return redirect('/home/')
        data = [(rollno[i:i + 2]) for i in range(0, len(rollno), 2)]
        year1 = datetime.datetime.today().year
        month1 = datetime.datetime.today().month
        sem = '1'
        if data[2] != '1A':
            data[0] = str(int(data[0]) - 1)
        if data[0] == '19' or data[0] == '18':
            if month1 >= 4:
                sem = '2'
        elif data[0] == '20' or data[0] == '21':
            if month1 >= 5:
                sem = '2'
        year1 = year1 - (2000 + int(data[0]))
        if year1 == 1 and not rollno in frdata:
            fdata.append(rollno)
        elif year1 == 2 and not rollno in sdata:
            sdata.append(rollno)
        elif year1 == 3 and not rollno in tdata:
            tdata.append(rollno)
        else:
            if not rollno in frdata:
                frdata.append(rollno)
        adyear = year_dic[str(year1) + sem]
        branch = branch_dic[data[3]]
        web.get('http://202.91.76.90:94/attendance/attendanceTillADate.php')
        link = web.current_url
        if link != 'http://202.91.76.90:94/attendance/attendanceTillADate.php':
            login(web)
        if data[3] == '12':
            sec = 1
            att = get_data(adyear, branch, sec, rollno)
        elif data[3] == '30' and int(year1) >= 2:
            sec = 1
            att = get_data(adyear, branch, sec, rollno)
        elif rollno in cache_data:
            sec = cache_data[rollno]
            att = get_data(adyear, branch, sec, rollno)

        else:
            for i in range(2, 5):
                att = get_data(adyear, branch, i, rollno)
                if att is None:
                    continue
                else:
                    break
        if att is None:
            att = 'ROLLNO NOT FOUND'
        if not rollno in cache_data:
            cache_data[rollno] = get_data.sec1
        return render_template('home.html', att=att, rollno=rollno,
                               info='Thank you for using our site. If there is any problem please send mail to ',
                               fdlink='attnbkrist@gmail.com')

    return redirect('/home/')


@app.route('/admin/')
def admin():
    if not session.get('name'):
        return render_template('admin.html')
    else:
        return redirect('/adminsuccess')


@app.route('/adminsuccess/', methods=['POST', 'GET'])
def adminsuccess():
    if request.method == 'POST':
        passw = request.form['adminpass']
        if (passw == 'nbkr@123'):
            session['name'] = 'adminlogin'
            return render_template('adminsuc.html', fdata=str(sorted(fdata)), fsize=len(fdata),
                                   sdata=str(sorted(sdata)), ssize=len(sdata),
                                   tdata=str(sorted(tdata)), tsize=len(tdata), frdata=str(sorted(frdata)),
                                   frsize=len(frdata),
                                   tdsize=len(fdata) + len(sdata) + len(tdata) + len(frdata))
        else:
            flash("Wrong password")
            return redirect('/admin/')
    else:
        return redirect('/admin/')


if __name__ == '__main__':
    app.run()
