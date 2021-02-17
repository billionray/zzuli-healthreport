from selenium import webdriver
import time,json,requests,smtplib
# 加载邮箱模块
from email.mime.text import MIMEText
from email.utils import formataddr
debug_mode=0 #调试模式
mail=1
##############信息填写################
#None
##############登录模块开始################
def service(username,password,mobile,homemobile,gpslocation,lat,lon,my_user,my_sender,SMTPdomain,SMTPauth,datetime):
    print(username)
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
    time.sleep(0.1)  # 加载等待
    #####登录模块以后函数化#######
    driver.find_element_by_xpath("./*//div[@class='p-r']/input").send_keys(username)  # 输入账号
    driver.find_element_by_xpath("//input[@class='qy-log-input form-control pasword']").send_keys(password)  # 输入密码
    time.sleep(0.1)
    driver.find_element_by_xpath("//input[@class='qy-log-btn is-on']").click  # 登录 方案一
    botton = 'document.getElementsByClassName("qy-log-btn is-on")[0].click();'
    driver.execute_script(botton)  # 登录 方案2
    time.sleep(0.1)
    ############登录模块结束####################

    #############肺炎打卡##################
    # botton= 'document.getElementsByClassName("mui-tab-item mui-active")[0].click();'
    # driver.execute_script(botton)#切换到肺炎打卡选项卡方案一
    # time.sleep(0.5)
    # botton= 'document.getElementsByClassName("mui-table-view-cell mui-media mui-col-xs-3 mui-col-sm-3")[0].click();'
    # driver.execute_script(botton) #切换到肺炎打卡选项卡方案二

    ##############链接获取开始################
    driver.get(肺炎打卡)  # 切换到肺炎打卡选项卡 方案三 以获取id

    for link in driver.find_elements_by_xpath("//*[@data-href]"):  # 获取data-href元素
        if debug_mode==1:
            print(link.get_attribute('data-href'))
        ###处理每日打卡链接
        dakaurl = link.get_attribute('data-href')

        getuserurl = dakaurl  ###截取code
        getuserurl = getuserurl.replace('view?from=h5&', 'get_user_info?') + "&wj_type=0"
        if debug_mode == 1:
            print(getuserurl)
    
        dakaurl = dakaurl + "&date=" + datetime
        ###结束
        driver.get(link.get_attribute('data-href') + "&date=" + datetime)  # 切换到每日打卡页面
        if debug_mode == 1:
            print(dakaurl)
        selenium_cookies = driver.get_cookies()
    time.sleep(0.1)

    ##############链接获取结束################
    ##############cookie处理及header处理开始################
    cookies = {}
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']

    #替换cookie中可能出现的%3D为等号
    xsrftoken=cookies.get("XSRF-TOKEN", )
    xxsrftoken=xsrftoken.replace('%3D','=')
    if debug_mode == 1:
        print(xxsrftoken)
    get_headers={
          "Connection": "keep-alive",
          "Accept": "application/json, text/plain, */*",
          "DNT": "1",
          "X-XSRF-TOKEN": xxsrftoken,
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Dest": "empty",
          "Referer": ("%s" % dakaurl),
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9",
          "Cookie": "PHPSESSID="+cookies["PHPSESSID"]+ ";XSRF-TOKEN=" + cookies["XSRF-TOKEN"] +";"+"laravel_session="+cookies["laravel_session"]
        }

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
    #data
    ##############cookie处理及header处理结束################
    ##############data字典处理开始################
    sourcedata = requests.get(getuserurl,headers=get_headers,cookies=cookies)
    sourcedata.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
    yuandata=sourcedata.text
    if debug_mode == 1:
        print(yuandata)
    user_dict = json.loads(yuandata)
    if debug_mode == 1:
        print(user_dict)
    data = {
        "user_code": user_dict.get("user_code", ), "user_name": user_dict.get("user_name", ), "id_card": user_dict.get("id_card", ), "date": datetime, "sex": user_dict.get("sex", ),
        "age": user_dict.get("age", ), "org": user_dict.get("org", ), "year": user_dict.get("year", ), "spec": user_dict.get("spec", ), "class": user_dict.get("class", ), "region": "", "area": "",
        "build": "", "dorm": "", "mobile": mobile, "jt_mobile": homemobile, "province": user_dict.get("province", ), "city": user_dict.get("city", ),
        "district": user_dict.get("district", ), "address": user_dict.get("address", ), "hjdz": user_dict.get("hjdz", ), "hj_province": user_dict.get("hj_province", ), "hj_city": user_dict.get("hj_city", ), "hj_district": user_dict.get("hj_district", ),
        "out": "否",
        "out_address": "[{\"start_date\":\"\",\"end_date\":\"\",\"province\":\"\",\"city\":\"\",\"district\":\"\",\"area\":\"\",\"address\":\"\"}]",
        "hb": "否", "hb_area": "", "hn": "否", "hn_area": "", "lat": lat, "lon": lon, "gcj_lat": lat,
        "gcj_lon": lon, "jz_address": gpslocation, "jz_province": user_dict.get("province", ), "jz_city": user_dict.get("city", ),
        "jz_district": user_dict.get("district", ), "jz_sfyz": "是", "sj_province": "", "sj_city": "", "sj_district": "", "temp": "正常",
        "jrzz": "无", "jzqk": "", "stzk": "无症状", "jcbl": "否", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "", "glp": "",
        "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "无", "hb_date": "", "jz_qzbl": "", "tz_qzbl": "",
        "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "", "jc_jcrq": "",
        "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "", "qz_yqbl": "否", "qz_yqrq": "",
        "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "", "zl_address": "", "zl_sfzy": "", "zl_zyrq": "",
        "xq_province": "", "xq_city": "", "xq_district": "", "xq_area": "", "xq_address": "", "home_time": "", "wj_type": 0
    }
    if debug_mode == 1:
        print(data)

    #####以下代码为post部分，未完成，完成部分可能有错误
    # 转换data字典类型为字符串类型并支持中文
    datajson = json.dumps(data, ensure_ascii=False)
    #print(datajson)
    ##############data字典处理结束################
    ##############邮箱配置开始################
    #my_sender = 发件人邮箱  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
    #my_user = 收件人邮箱  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
    #定义邮件函数
    def mail(yesorno):
        ret = True
        try:
            msg = MIMEText(user_dict.get("user_code", ) + ':' + '打卡' + yesorno + '！', 'plain', 'utf-8')
            msg['From'] = formataddr(["打卡提醒", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["您好，订阅者", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "打卡"+yesorno  # 主题

            server = smtplib.SMTP_SSL(SMTPdomain, 465)  # 使用SSL发送
            server.login(my_sender, SMTPauth)  # SMTP密码，这里是我的的密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            server.quit()
        except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
            ret = False
        return ret
    ##############邮箱配置结束################
    ##############发送请求！！！################
    r=requests.post("http://msg.zzuli.edu.cn/xsc/add", data=datajson.encode(), cookies=cookies, headers=headers)
    ##############检测结果并发送邮件################
    driver.quit()
    if r.status_code ==200:
        print("---------------DAKA Success---------------")
        ret = mail("成功")
        if ret:
            print("mail ok")
            return'daka ok mail ok '
        else:
            print("mail failed")
            return 'daka ok mail faild'

    else:
        print("Retry!")
        retry = requests.post("http://msg.zzuli.edu.cn/xsc/add", data=datajson.encode(), cookies=cookies, headers=headers)
        if retry.status_code == 200:
            print("---------------DAKA Success---------------")
            ret = mail("成功")
            if ret:
                print("mail ok")
                return 'daka ok mail ok '
            else:
                print("mail failed")
                return 'daka ok mail faild'
        else:
            print("Mission Failed,Check network or server now")
            ret = mail("失败")
            if ret:
                print("mail ok")
                return'daka faild mail faild'
            else:
                print("mail failed")
                return'daka faild mail faild'
    #结束所有进程，以免内存占用过高

if __name__=='__main__':
    service()