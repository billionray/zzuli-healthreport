from selenium import webdriver
import time
import json
import requests
import smtplib  # 加载邮箱模块
from email.mime.text import MIMEText
from email.utils import formataddr
datetime = time.strftime("%Y-%m-%d", time.localtime())  # 获取日期 YY-MM-DD
debug_mode=0 #调试模式
##############以上勿动################
日期=datetime
用户名 = ""
密码 = ""
姓名=""
身份证号=""
性别=""
年龄=19
学院=""
年级=2020
专业=""
班级=""
电话=""
家庭电话=""
省=""
市=""
区县=""
地址=""
GPS地址=""
经度=223.22332 #小数点后五位
纬度=223.22332  #小数点后五位
收件人邮箱=""
发件人邮箱=""
发件人密码=""
发件服务器SMTP地址=""
##############以下勿动################
print(姓名)
data = {
    "user_code": 用户名, "user_name": 姓名, "id_card": 身份证号, "date": 日期, "sex": 性别,
    "age": 年龄, "org": 学院, "year": 年级, "spec": 专业, "class": 班级, "region": "", "area": "",
    "build": "", "dorm": "", "mobile": 电话, "jt_mobile": 家庭电话, "province": 省, "city": 市,
    "district": 区县, "address": 地址, "hjdz": "", "hj_province": "", "hj_city": "", "hj_district": "",
    "out": "否",
    "out_address": "[{\"start_date\":\"\",\"end_date\":\"\",\"province\":\"\",\"city\":\"\",\"district\":\"\",\"area\":\"\",\"address\":\"\"}]",
    "hb": "否", "hb_area": "", "hn": "否", "hn_area": "", "lat": 经度, "lon": 纬度, "gcj_lat": 经度,
    "gcj_lon": 纬度, "jz_address": GPS地址, "jz_province": 省, "jz_city": 市,
    "jz_district": 区县, "jz_sfyz": "是", "sj_province": "", "sj_city": "", "sj_district": "", "temp": "正常",
    "jrzz": "无", "jzqk": "", "stzk": "无症状", "jcbl": "否", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "", "glp": "",
    "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "", "hb_date": "", "jz_qzbl": "", "tz_qzbl": "",
    "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "", "jc_jcrq": "",
    "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "", "qz_yqbl": "否", "qz_yqrq": "",
    "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "", "zl_address": "", "zl_sfzy": "", "zl_zyrq": "",
    "xq_province": "", "xq_city": "", "xq_district": "", "xq_area": "", "xq_address": "", "home_time": "", "wj_type": 0
}

loginurl = "http://kys.zzuli.edu.cn/cas/login?"
肺炎打卡 = "https://msg.zzuli.edu.cn/xsc/view?from=h5"

opt = webdriver.ChromeOptions()  # 创建浏览器
if debug_mode == 0:
    opt.add_argument('headless')
    opt.add_argument('no-sandbox')
    opt.add_argument('disable-dev-shm-usage')
driver = webdriver.Chrome(options=opt)  # 创建浏览器对象
driver.get(loginurl)  # 打开网页
# driver.maximize_window()                      #最大化窗口
time.sleep(0.5)  # 加载等待
#####登录模块以后函数化#######
driver.find_element_by_xpath("./*//div[@class='p-r']/input").send_keys(用户名)  # 输入账号
driver.find_element_by_xpath("//input[@class='qy-log-input form-control pasword']").send_keys(密码)  # 输入密码
time.sleep(0.5)
driver.find_element_by_xpath("//input[@class='qy-log-btn is-on']").click  # 登录 方案一
botton = 'document.getElementsByClassName("qy-log-btn is-on")[0].click();'
driver.execute_script(botton)  # 登录 方案2
time.sleep(0.5)
############登录模块结束####################

#############肺炎打卡##################
# botton= 'document.getElementsByClassName("mui-tab-item mui-active")[0].click();'
# driver.execute_script(botton)#切换到肺炎打卡选项卡方案一
# time.sleep(0.5)
# botton= 'document.getElementsByClassName("mui-table-view-cell mui-media mui-col-xs-3 mui-col-sm-3")[0].click();'
# driver.execute_script(botton) #切换到肺炎打卡选项卡方案二


driver.get(肺炎打卡)  # 切换到肺炎打卡选项卡 方案三 以获取id

for link in driver.find_elements_by_xpath("//*[@data-href]"):  # 获取data-href元素
    if debug_mode==1:
        print(link.get_attribute('data-href'))
    ###处理每日打卡链接
    dakaurl = link.get_attribute('data-href')

    dakaurl = dakaurl + "&date=" + datetime
    ###结束
    driver.get(link.get_attribute('data-href') + "&date=" + datetime)  # 切换到每日打卡页面
    if debug_mode == 1:
        print(dakaurl)
    selenium_cookies = driver.get_cookies()
time.sleep(0.5)
# cookie处理
cookies = {}
for cookie in selenium_cookies:
    cookies[cookie['name']] = cookie['value']

#替换cookie中可能出现的%3D为等号
xsrftoken=cookies.get("XSRF-TOKEN", )
xxsrftoken=xsrftoken.replace('%3D','=')
if debug_mode == 1:
    print(xxsrftoken)
headers = {
    "Connection": "keep-alive",
    "X-XSRF-TOKEN": xxsrftoken,
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Content-Type":"application/json;charset=UTF-8",
    "Origin":"https://msg.zzuli.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": ("%s" % dakaurl),
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "PHPSESSID="+cookies["PHPSESSID"]+ ";XSRF-TOKEN=" + cookies["XSRF-TOKEN"] +";"+"laravel_session="+cookies["laravel_session"]
}
if debug_mode == 1:
    print(headers)
#"Cookie": "laravel_session="+cookies["laravel_session"]+ ","+ "PHPSESSID="+cookies["PHPSESSID"]+ ","+ "XSRF-TOKEN=" + cookies["XSRF-TOKEN"]
# headers未完成
# 其中，headers中的“X-XSRF-TOKEN”需要从Cookies提取，对应着cookies中的“XSRF-TOKEN”

#####以下代码为post部分，未完成，完成部分可能有错误
# 转换data字典类型为字符串类型并支持中文
datajson = json.dumps(data, ensure_ascii=False)
#print(datajson)

#邮箱配置
my_sender = 发件人邮箱  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user = 收件人邮箱  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
#定义邮件函数
def mail(yesorno):
    ret = True
    try:
        msg = MIMEText(姓名+':'+'打卡'+ yesorno +'！', 'plain', 'utf-8')
        msg['From'] = formataddr(["打卡提醒", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["您好，订阅者", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "打卡"+yesorno  # 主题

        server = smtplib.SMTP_SSL(发件服务器SMTP地址, 465)  # 使用SSL发送
        server.login(my_sender, 发件人密码)  # SMTP密码，这里是我的的密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    return ret

r=requests.post("http://msg.zzuli.edu.cn/xsc/add", data=datajson.encode(), cookies=cookies, headers=headers)
r.status_code
if r.status_code ==200:
    print("---------------DAKA Success---------------")
    ret = mail("成功")
    if ret:
        print("mail ok")
    else:
        print("mail failed")

else:
    print("Mission Failed,Check network or server now")
    ret = mail("失败")
    if ret:
        print("mail ok")
    else:
        print("mail failed")
#结束所有进程，以免内存占用过高
driver.quit()
