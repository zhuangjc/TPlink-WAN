#! /usr/bin/python2
# coding=utf-8
from time import sleep
import smtplib
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


# 获取IP地址
def ip_request():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = Firefox(executable_path='C:\geckodriver', firefox_options=options)  # 使用headless+Firefox

    driver.get('http://admin:admin@192.168.1.1')  # 打开页面
    sleep(2)

    driver.switch_to_frame("mainFrame")  # 转到IP所在frame
    elem_dh = driver.find_elements_by_xpath(
        "/html/body/center/form/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[2]")
    ip_req = elem_dh[0].text
    driver.quit()
    return ip_req


# 检查获取的IP与保存的IP是否一致，不一致代表IP改变
def ip_check(new):
    IP = open('ip_save.txt', 'r')
    old = str(IP.read())
    IP.close()
    return new == old, old


# 规范邮件格式
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr))


# 发送邮件
def send_mail(new_ip, old_ip):
    from_addr = '1017010330@njupt.edu.cn'
    password = '182815'  # 输入SMTP服务器地址:
    smtp_server = 'mail.163.com'  # 输入收件人地址:
    to_addr = '1017010330@njupt.edu.cn'

    msg = MIMEText('路由器IP地址从 ' + old_ip + ' 变为 ' + new_ip + ' !', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'TP-LINK <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'IP地址改变', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


new = str(ip_request())
check, old = ip_check(new)
print(check)
if check is False:
    send_mail(new, old)
    file = open("ip_save.txt", 'w')
    file.write(new)
    file.close()




