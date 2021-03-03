import time
import os
from main import service
from notification import mail

datetime = time.strftime("%Y-%m-%d", time.localtime())
datetime = datetime  # 日期 如果需要更改请遵循这个格式："YY-MM-DD"

#############################
# 是否需要邮件提醒             #
#############################

try:
    mail_flag = float(os.environ['MAILFLAG'])  # 不可改动
except:
    mail_flag = 0  # 若需要邮箱提醒请修改为1

#############################
# 基础信息填写                #
#############################

try:
    username = os.environ['USERNAME']  # 不可改动
    password = os.environ['PASSWORD']  # 不可改动
    mobile = os.environ['MOBILE']  # 不可改动
    homemobile = os.environ['HOMEMOBILE']  # 不可改动
    reporttype = os.environ['REPORTTYPE']  # 不可改动
except:
    username = ""  # 学号
    password = ""  # i轻工大密码，默认为zzuli+身份证后六位
    mobile = ""  # 电话
    homemobile = ""  # 家庭电话
    reporttype = ""  # 打卡类型，请填写home(居家打卡)morn(晨检打卡)dorm(归寝打卡)

#############################
# 居家打卡信息填写             #
#############################

try:
    gpslocation = os.environ['GPS']  # 不可改动
    lat = float(os.environ['LAT'])  # 不可改动
    lon = float(os.environ['LON'])  # 不可改动
except:
    gpslocation = ""  # 家庭GPS地址，详细一点，例如：XX省XX市XX区XX街道XX小区(可选)
    # 经纬度查询： https://lbs.amap.com/console/show/picker
    # 部分手机内置指南针也可查询经纬度
    lat = ""  # 纬度 小数点后五位
    lon = ""  # 精度 小数点后五位

#############################
# 在校打卡信息填写             #
#############################

try:
    region = os.environ['REGION']  # 不可改动
    area = os.environ['AREA']  # 不可改动
    build = os.environ['BUILD']  # 不可改动
    dorm = os.environ['DORM']  # 不可改动
    schoolgps = os.environ['SCHOOLGPS']  # 不可改动
    schoollat = os.environ['SCHOOLLAT']  # 不可改动
    schoollon = os.environ['SCHOOLLON']  # 不可改动
except:
    # 此处请对应官方打卡页面填写，保证和官方打卡页写的一样
    region = ""  # 校区 例：东风校区、科学校区、禹州实习训练基地、校外走读
    area = ""  # 例：宿舍区 一区、二区、秋实区、丰华区
    build = ""  # 例：楼号 5号楼、1号楼
    dorm = ""  # 宿舍号（仅数字）
    schoolgps = ""  # 学校GPS地址，详细一点，例如：河南省郑州市金水区郑州轻工业大学第二学生园区
    # 经纬度查询： https://lbs.amap.com/console/show/picker
    # 部分手机内置指南针也可查询经纬度
    schoollat = ""  # 纬度 小数点后五位
    schoollon = ""  # 精度 小数点后五位

#############################
# 邮件提醒信息填写（可选）       #
#############################

try:
    my_user = os.environ['MYUSER']  # 不可改动
    my_sender = os.environ['MYSENDER']  # 不可改动
    SMTPdomain = os.environ['SMTPDOMAIN']  # 不可改动
    SMTPauth = os.environ['SMTPAUTH']  # 不可改动
except:
    my_user = ""  # 收件人
    my_sender = ""  # 发件人
    SMTPdomain = ""  # 发件人SMTP地址（SSL）
    SMTPauth = ""  # 发件人SMTP授权码

run = service(username, password, mobile, homemobile, gpslocation, lat, lon, datetime, reporttype, region, area, build,dorm,schoolgps,schoollat,schoollon)

if run == 1:
    reportstatus = 1  # 这里是为了以后方便加入retry和其它通知方式
    print("mission success")
else:
    reportstatus = 0
    print("mission faild")

if mail_flag == 1:
    if reportstatus == 1:
        mail(username, "成功", my_user, my_sender, SMTPdomain, SMTPauth, datetime,reporttype)
        print("mail success")
    else:
        mail(username, "失败", my_user, my_sender, SMTPdomain, SMTPauth, datetime,reporttype)
        print("mail faild")

else:
    print("未开启")
