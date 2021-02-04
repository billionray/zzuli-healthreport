from selenium import webdriver
import time
import re
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
    纬度: 113.27854, "jz_address": GPS地址, "jz_province": 省, "jz_city": 市,
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
    #print(a)
    selenium_cookies = driver.get_cookies()
time.sleep(0.5)
# cookie处理
cookies = {}
for cookie in selenium_cookies:
    cookies[cookie['name']] = cookie['value']
