import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import requests
'''
this module can notify u the report starus by different ways
if you are not developer,you must NOT write anything in this file
'''


def mail(username, yesorno, my_user, my_sender, SMTPdomain, SMTPauth, datetime, reporttype):
    ret = True
    if reporttype == "home":
        type = "居家"
    elif reporttype == "morn":
        type = "健康"
    elif reporttype == "dorm":
        type = "归寝"
    data_json = {
        "username": username,
        "state": yesorno,
        "type": type,
    }
    html_data = requests.post("http://daka_email.xwwwb.com/api", data=data_json).text
    try:
        msg = MIMEText(html_data, 'html', 'utf-8')
        msg['From'] = formataddr(["打卡提醒", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["您好，订阅者", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡通知上新啦！打开看看吧！"  # 主题
        server = smtplib.SMTP_SSL(SMTPdomain, 465)  # 使用SSL发送
        server.login(my_sender, SMTPauth)  # SMTP密码，这里是我的的密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    return ret
