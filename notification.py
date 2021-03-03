import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def mail(username,yesorno,my_user,my_sender,SMTPdomain,SMTPauth,datetime,reporttype):
    ret = True
    if reporttype == "home":
        type = "居家"
    elif reporttype == "morn":
        type = "晨检"
    elif reporttype == "dorm":
        type = "归寝"
    try:
        msg = MIMEText(username+':' + type + '打卡' ':'+ yesorno + '！', 'plain', 'utf-8')
        msg['From'] = formataddr(["打卡提醒", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["您好，订阅者", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = datetime+type+"打卡"+yesorno  # 主题
        server = smtplib.SMTP_SSL(SMTPdomain, 465)  # 使用SSL发送
        server.login(my_sender, SMTPauth)  # SMTP密码，这里是我的的密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    return ret