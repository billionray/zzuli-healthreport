import time
from Services import service
datetime = time.strftime("%Y-%m-%d", time.localtime())  # 获取日期 YY-MM-DD
datetime=datetime #日期 需要更改格式：YY-MM-DD 
username = "" #用户名
password= "" #密码
mobile="" #电话
homemobile="" #家庭电话
gpslocation="" #GPS地址，详细一点，例如：XX省XX市XX区XX街道XX小区
# 经纬度查询： https://lbs.amap.com/console/show/picker
lat=23.23333#小数点后五位 #经度
lon=233.23333  #小数点后五位 #纬度
#以下信息可以不用填写，不填写则无法使用邮箱提醒
my_user="" #收件人
my_sender="" #发件人
SMTPdomain="" #发件人SMTP地址（SSL）
SMTPauth="" #发件人SMTP授权码
service(username,password,mobile,homemobile,gpslocation,lat,lon,my_user,my_sender,SMTPdomain,SMTPauth,datetime)
