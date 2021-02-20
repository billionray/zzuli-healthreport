import time
import os
from main import service
from notification import mail
datetime = time.strftime("%Y-%m-%d", time.localtime())
datetime=datetime #日期 如果需要更改请遵循这个格式："YY-MM-DD" 
number_of_retries=3 #重试次数
mail=1
# 经纬度查询： https://lbs.amap.com/console/show/picker
try:
    username = os.environ['USERNAME'] 
    password= os.environ['PASSWORD'] 
    mobile=os.environ['MOBILE'] 
    homemobile=os.environ['HOMEMOBILE'] 
    gpslocation=os.environ['GPS'] 
    lat=float(os.environ['LAT'])
    lon=float(os.environ['LON']) 

except:
    username = "" #用户名
    password= "" #密码
    mobile="" #电话
    homemobile="" #家庭电话
    gpslocation="" #GPS地址，详细一点，例如：XX省XX市XX区XX街道XX小区(可选)
    # 经纬度查询： https://lbs.amap.com/console/show/picker
    lat=23.23333#小数点后五位 #经度
    lon=233.23333  #小数点后五位 #纬度
#以下可选
try:
    my_user=os.environ['USER']
    my_sender=os.environ['SENDER']
    SMTPdomain=os.environ['SMTPDOMAIN']
    SMTPauth=os.environ['SMTPAUTH']
except:
    my_user="" #收件人
    my_sender="" #发件人
    SMTPdomain="" #发件人SMTP地址（SSL）
    SMTPauth="" #发件人SMTP授权码

run=service(username,password,mobile,homemobile,gpslocation,lat,lon,datetime)
if run==1:
   reportstatus=1 #这里是为了以后方便加入retry和其它通知方式
else:
   reportstatus=0
if mail==1:
    if reportstatus==1:
        mail("成功",my_user,my_sender,SMTPdomain,SMTPauth,datetime)
    else:
        mail("失败",my_user,my_sender,SMTPdomain,SMTPauth,datetime)

else:
    print("未开启")
