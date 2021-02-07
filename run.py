import time
from Services import service
datetime = time.strftime("%Y-%m-%d", time.localtime())  # 获取日期 YY-MM-DD
日期=datetime
用户名=username = ""
密码=password= ""
电话=mobile=""
家庭电话=homemobile=""
GPS地址=gpslocation=""
经度=lat=23.23333#小数点后五位
纬度=lon=233.23333  #小数点后五位
收件人=my_user=""
发件人=my_sender=""
SMTP地址=SMTPdomain=""
SMTP授权码=SMTPauth=""
service(username,password,mobile,homemobile,gpslocation,lat,lon,my_user,my_sender,SMTPdomain,SMTPauth,datetime)