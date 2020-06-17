# coding=UTF-8
# 邮件服务集

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tokens import Verify

# 第三方 SMTP 服务
mail_host="smtp.qq.com"  # 设置服务器
mail_user="cloud.limo1029@qq.com"    # 用户名
mail_pass="wyqqlhlrglwkdegj"   # 口令


sender = 'cloud@limo1029.com'   # 发送人
receivers = ['limo1029@qq.com']  # 接收邮件组

mail_msg = '<p>测试</p><p>您的验证码为：' + Verify.EmailCheckToken() + '</P>'
    
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header('cloud.limo1029', 'utf-8')
message['To'] = Header('test', 'utf-8')


smtpObj = smtplib.SMTP()
smtpObj.connect(mail_host, 465)
smtpObj.login(mail_user, mail_pass)
smtpObj.sendmail(sender, receivers, message.as_string())
print('ok')