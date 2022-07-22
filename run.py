import json
import os
import time

from app.encode import encode
from app.main import service
from app.notification import mail

'''
this module can provide you different ways to transport the information to the program
'''
datetime = time.strftime("%Y-%m-%d", time.localtime())
datetime = datetime


with open("data.json", 'r', encoding='UTF-8') as f:
    load_dict = json.load(f)

try:
    notice_type = float(os.environ['NOTICETYPE'])
except:
    notice_type = float(load_dict.get("noticetype", ))

nowtime = time.strftime("%H", time.localtime())
nowtime = int(nowtime)
print(f"当前时间{nowtime}时 \n")
report_type = "morn"
if 0 <= nowtime < 20:
    report_type = "morn"
elif 20 <= nowtime <= 24:
    report_type = "dorm"

try:
    home = float(os.environ['HOME'])
except:
    home = float(load_dict.get("home", ))

if home == 1:
    report_type = "home"

if report_type == "morn":
    print("开始晨间打卡\n")
elif report_type == "dorm":
    print("开始归寝打卡\n")
elif report_type == "home":
    print("开始居家打卡\n")

try:
    username = os.environ['USERNAME'] 
    password = os.environ['PASSWORD'] 
    mobile = os.environ['MOBILE'] 
    homemobile = os.environ['HOMEMOBILE'] 
except:

    username = load_dict.get("username", )
    password = load_dict.get("password", )
    mobile = load_dict.get("mobile", )
    homemobile = load_dict.get("homemobile", )

try:
    gpslocation = os.environ['GPS'] 
    lat = float(os.environ['LAT']) 
    lon = float(os.environ['LON']) 
except:
    gpslocation = load_dict.get("gpslocation", )
    lat = float(load_dict.get("lat", ))
    lon = float(load_dict.get("lon", ))
try:
    vaccine = os.environ['VACCINE']
    #nucleicacidtest = os.environ['NUCLEICACIDTEST']
    lasttest = os.environ['LASTTEST']

except:
    vaccine = load_dict.get("vaccine", )
    #nucleicacidtest = load_dict.get("nucleicacidtest", )
    lasttest = load_dict.get("lasttest", )
try:
    novaccine_reason=os.environ['NOVACCINEREASON']
    novaccine_detail=os.environ['NOVACCINEDETAIL']
except:
    try:
        novaccine_reason = load_dict.get("novaccine_reason", )
        novaccine_detail = load_dict.get("novaccine_detail", )
    except:
        novaccine_reason = ""
        novaccine_detail = ""

try:
    region = os.environ['REGION']
    area = os.environ['AREA']
    build = os.environ['BUILD']
    dorm = os.environ['DORM']
    schoolgps = os.environ['SCHOOLGPS']
    schoollat = os.environ['SCHOOLLAT']
    schoollon = os.environ['SCHOOLLON']
except:
    region = load_dict.get("region", )
    area = load_dict.get("area", )
    build = load_dict.get("build", )
    dorm = load_dict.get("dorm", )
    schoolgps = load_dict.get("schoolgps", )
    schoollat = load_dict.get("schoollat", )
    schoollon = load_dict.get("schoollon", )

try:
    my_user = os.environ['MYUSER']
    my_sender = os.environ['MYSENDER']
    SMTPdomain = os.environ['SMTPDOMAIN']
    SMTPauth = os.environ['SMTPAUTH']
except:
    my_user = load_dict.get("my_user", )
    my_sender = load_dict.get("my_sender", )
    SMTPdomain = load_dict.get("SMTPdomain", )
    SMTPauth = load_dict.get("SMTPauth", )
history_url = encode(username)
# print(history_url)

nucleicacidtest=""
run = 0

data = [mobile, homemobile, gpslocation, lat, lon, region, area, build, dorm, schoolgps, schoollat, schoollon, vaccine,
        nucleicacidtest, lasttest,novaccine_reason,novaccine_detail]
try:
    run = service(username, password, datetime, report_type, data)
except:
    pass

if run == 1:
    report_status = 1  # 这里是为了以后方便加入retry和其它通知方式
    print("打卡成功")
else:
    report_status = 0
    print("打卡失败")

if notice_type == 1:
    if report_status == 1:
        mail(username, "成功", history_url, my_user, my_sender, SMTPdomain, SMTPauth, datetime, report_type)
        print("打卡成功，已发送邮件")
    else:
        mail(username, "失败", history_url, my_user, my_sender, SMTPdomain, SMTPauth, datetime, report_type)
        print("打卡失败，已发送邮件")
else:
    print("未开启通知")
