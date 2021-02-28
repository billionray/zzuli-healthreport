import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def mail(yesorno,my_user,my_sender,SMTPdomain,SMTPauth,datetime):
    ret = True
    try:
        msg = MIMEText(user_dict.get("user_code", ) + ':' + '打卡' + yesorno + '！', 'plain', 'utf-8')
        msg['From'] = formataddr(["打卡提醒", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["您好，订阅者", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = datetime+reporttype+"打卡"+yesorno+username  # 主题
        server = smtplib.SMTP_SSL(SMTPdomain, 465)  # 使用SSL发送
        server.login(my_sender, SMTPauth)  # SMTP密码，这里是我的的密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    return ret