import time

from selenium import webdriver

web = webdriver.Chrome(executable_path='static/chromedriver')
web.implicitly_wait(10)
web.get('http://202.91.76.90:94/attendance/attendanceTillADate.php')
user=web.find_element_by_xpath('//*[@id="username"]')
user.send_keys('jyothsna5')
passw=web.find_element_by_xpath('//*[@id="password"]')
passw.send_keys('mayashijo')

sub=web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[6]/td/input')
sub.click()
year=web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/select/option[6]')
year.click()
bran=web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[3]/select/option[10]')
bran.click()
show=web.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr[2]/td[5]/input[2]')
show.click()
att=web.find_element_by_xpath('//*[@id="19KB1A1244"]')
a=att.text.split('\n')
web.close()

print(a[0][-5:])

