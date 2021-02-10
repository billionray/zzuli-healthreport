import time
from Services import service
datetime = time.strftime("%Y-%m-%d", time.localtime())  # 获取日期 YY-MM-DD
datetime=datetime #日期 需要更改格式：YY-MM-DD 
username = "" #用户名
password= "" #密码
mobile="" #电话
homemobile="" #家庭电话
gpslocation="" #GPS地址
lat=23.23333#小数点后五位 #经度
lon=233.23333  #小数点后五位 #纬度
my_user="" #收件人
my_sender="" #发件人
SMTPdomain="" #SMTP地址
SMTPauth="" #SMTP授权码
service(username,password,mobile,homemobile,gpslocation,lat,lon,my_user,my_sender,SMTPdomain,SMTPauth,datetime)