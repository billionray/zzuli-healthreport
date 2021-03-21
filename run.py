import time
import os
from main import service
from notification import mail
from encode import encode
import json

'''
this module can provide you diffrent ways to transport the information to the program
'''
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

# self_dir = os.path.dirname(__file__)
# self_dir = self_dir + "\data.json"
# print(self_dir)
# with open(self_dir, 'r', encoding='UTF-8') as f:
#     load_dict = json.load(f)
# username = load_dict.get("username", )
# password = load_dict.get("password", )

# 获取时间判断是晨检还是归寝
nowtime = time.strftime("%H", time.localtime())
nowtime = int(nowtime)
print(f"当前时间{nowtime}时 \n")
if (nowtime>4 and nowtime<11):
    print("执行晨检打卡！\n")
    reporttype = "morn"
elif(nowtime>18 and nowtime <23):
    print("执行归寝打卡！\n")
    reporttype = "dorm"

home=0 # 将其改为1启用居家打卡
if (home) == 1:
    reporttype = "home"


try:
    username = os.environ['USERNAME']  # 不可改动
    password = os.environ['PASSWORD']  # 不可改动
    mobile = os.environ['MOBILE']  # 不可改动
    homemobile = os.environ['HOMEMOBILE']  # 不可改动
except:
    username = ""  # 学号
    password = ""  # i轻工大密码，默认为zzuli+身份证后六位
    mobile = ""  # 电话
    homemobile = ""  # 家庭电话

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
    lat = 33.00000  # 纬度 小数点后五位 输入时无引号
    lon = 113.00000  # 精度 小数点后五位 输入时无引号

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
    schoollat = 33.00000  # 纬度 小数点后五位 输入时无引号
    schoollon = 113.00000  # 精度 小数点后五位 输入时无引号

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
historyurl = encode(username)
print(historyurl)
run = 0
try:
    run = service(username, password, mobile, homemobile, gpslocation, lat, lon, datetime, reporttype, region, area,
                  build, dorm, schoolgps, schoollat, schoollon)
except:
    pass

if run == 1:
    reportstatus = 1  # 这里是为了以后方便加入retry和其它通知方式
    print("mission success")
else:
    reportstatus = 0
    print("mission faild")

if mail_flag == 1:
    if reportstatus == 1:
        mail(username, "成功", historyurl, my_user, my_sender, SMTPdomain, SMTPauth, datetime, reporttype)
        print("打卡成功，已发送邮件")
    else:
        mail(username, "失败", historyurl, my_user, my_sender, SMTPdomain, SMTPauth, datetime, reporttype)
        print("打卡失败，已发送邮件")

else:
    print("未开启")
