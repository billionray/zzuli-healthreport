import time
import os
from main import service
from notification import mail
datetime = time.strftime("%Y-%m-%d", time.localtime())
datetime=datetime #日期 如果需要更改请遵循这个格式："YY-MM-DD" 
try:
    mail_flag = float(os.environ['MAILFLAG'])
except:
    mail_flag=0
# 经纬度查询： https://lbs.amap.com/console/show/picker
try:
    username = os.environ['USERNAME'] 
    password= os.environ['PASSWORD'] 
    mobile=os.environ['MOBILE'] 
    homemobile=os.environ['HOMEMOBILE'] 
    gpslocation=os.environ['GPS'] 
    lat=float(os.environ['LAT'])
    lon=float(os.environ['LON']) 
    reporttype=os.environ['REPORTTYPE']
except:
    username = "" #用户名
    password= "" #密码
    mobile="" #电话
    homemobile="" #家庭电话
    gpslocation="" #GPS地址，详细一点，例如：XX省XX市XX区XX街道XX小区(可选)
    # 经纬度查询： https://lbs.amap.com/console/show/picker 
    # 部分手机内置指南针也可查询经纬度
    lat=23.23333#小数点后五位 #纬度
    lon=233.23333  #小数点后五位 #经度
    reporttype="" #home/morn/dorm
try:
    inf=os.environ['INF']
except:
    region=""
    area=""
    build=""
    dorm=""
else:
    region=inf.split('.',4)[0]
    area=inf.split('.',4)[1]
    build=inf.split('.',4)[2]
    dorm=inf.split('.',4)[3]
#以下可选
try:
    my_user=os.environ['MYUSER']
    my_sender=os.environ['MYSENDER']
    SMTPdomain=os.environ['SMTPDOMAIN']
    SMTPauth=os.environ['SMTPAUTH']
except:
    my_user="" #收件人
    my_sender="" #发件人
    SMTPdomain="" #发件人SMTP地址（SSL）
    SMTPauth="" #发件人SMTP授权码


run=service(username,password,mobile,homemobile,gpslocation,lat,lon,datetime,reporttype,region,area,build,dorm)


if run==1:
   reportstatus=1 #这里是为了以后方便加入retry和其它通知方式
   print("mission success")
else:
   reportstatus=0
   print("mission faild")

if mail_flag==1:
    if reportstatus==1:
        mail(username,"成功",my_user,my_sender,SMTPdomain,SMTPauth,datetime)
        print("mail success")
    else:
        mail(username,"失败",my_user,my_sender,SMTPdomain,SMTPauth,datetime)
        print("mail faild")

else:
    print("未开启")
