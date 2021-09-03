#!/usr/bin/env python
# coding=utf-8


import smtplib
import email.mime.multipart
import email.mime.text
import random

def sendVerifCode(receiver):
    code=''
    for i in range(6):
        code=code + str(random.randint(0,9))
    print(code)

    #sender='yunge_jlu@sina.com'
    #server='smtp.sina.com'
    #passwd='145024'
    #sender='15543770273@163.com'
    #server='smtp.163.com'
    #passwd='13212661081liguo'
    #port='25'
    sender='1450246370@qq.com'
    server='smtp.qq.com'
    passwd='rlyvgeegmsddfihi'
    port='465'

    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = '来自PHM平台的验证码'
    msg['From'] = sender
    msg['To'] = receiver
    content = '''
    亲爱的用户您好，您本次的验证码为'''+code+'''
    本验证码五分钟内有效,请勿将其泄露给他人
    '''
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)
    #smtp = smtplib.SMTP()
    #smtp.connect(server, port)
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtp.login(sender, passwd)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('邮件发送成功email has send out !')
    return code

if __name__ == '__main__':
    objAddr='1450246370@qq.com'
    sendVerifCode(objAddr)
