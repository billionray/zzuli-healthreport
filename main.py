import json
import requests
import time
from selenium import webdriver
from retrying import retry
#from  run import number_of_retries
##############信息填写################
#None
##############登录模块开始################
@retry(stop_max_attempt_number=3)
def service(username,password,mobile,homemobile,gpslocation,lat,lon,datetime,reporttype,region,area,build,dorm):

    print(username)
    loginurl = "http://kys.zzuli.edu.cn/cas/login?"
    肺炎打卡 = "https://msg.zzuli.edu.cn/xsc/view?from=h5"

    opt = webdriver.ChromeOptions()  # 创建浏览器
    opt.add_argument('headless')
    opt.add_argument('no-sandbox')
    opt.add_argument('disable-dev-shm-usage')
    driver = webdriver.Chrome(options=opt)  # 创建浏览器对象
    driver.get(loginurl)  
    # driver.maximize_window()                      #最大化窗口
    time.sleep(0.1)  # 加载等待
    #####登录模块以后函数化#######
    driver.find_element_by_xpath("./*//div[@class='p-r']/input").send_keys(username)  # 输入账号
    driver.find_element_by_xpath("//input[@class='qy-log-input form-control pasword']").send_keys(password)  # 输入密码
    time.sleep(0.1)
    driver.find_element_by_xpath("//input[@class='qy-log-btn is-on']").click  # 登录
    botton = 'document.getElementsByClassName("qy-log-btn is-on")[0].click();'
    driver.execute_script(botton)  # 登录
    time.sleep(0.1)
    ############登录模块结束####################

    #############肺炎打卡##################
    # botton= 'document.getElementsByClassName("mui-tab-item mui-active")[0].click();'
    # driver.execute_script(botton)
    # time.sleep(0.5)
    # botton= 'document.getElementsByClassName("mui-table-view-cell mui-media mui-col-xs-3 mui-col-sm-3")[0].click();'
    # driver.execute_script(botton)

    ##############链接获取开始################
    driver.get(肺炎打卡)

    for link in driver.find_elements_by_xpath("//*[@data-href]"):  # 获取data-href元素

        ###处理每日打卡链接
        dakaurl = link.get_attribute('data-href')
        getuserurl = dakaurl  ###截取学校储存的data
        getuserurl = getuserurl.replace('view?from=h5&', 'get_user_info?') + "&wj_type=0"
        if reporttype=="home":
            dakaurl = dakaurl + "&date=" + datetime
        elif reporttype=="morn":
            dakaurl = dakaurl + "&date=" + datetime
            dakaurl=dakaurl.replace('xsc', 'morn')
            getuserurl=getuserurl.replace('&wj_type=0', '&wj_type=1')
        elif reporttype=="dorm":
            dakaurl = dakaurl + "&date=" + datetime
            dakaurl=dakaurl.replace('xsc', 'dorm')
        ###结束

        #get cookie
        driver.get(dakaurl + "&date=" + datetime)
        time.sleep(1)
        selenium_cookies = driver.get_cookies()

    ##############链接获取结束################
    ##############cookie处理及header处理开始################
    cookies = {}
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']

    #替换cookie中可能出现的%3D为等号
    xsrftoken=cookies.get("XSRF-TOKEN", )
    xxsrftoken=xsrftoken.replace('%3D','=')

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
    ##############cookie处理及header处理结束################
    ##############data字典处理开始################
    sourcedata = requests.get(getuserurl,headers=get_headers,cookies=cookies)
    sourcedata.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。
    yuandata=sourcedata.text
    user_dict = json.loads(yuandata)
    homedata = {
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
    morndata={
        "user_code":user_dict.get("user_code", ),
        "user_name":user_dict.get("user_name", ),
        "id_card":user_dict.get("id_card", ),
        "date":datetime,"sex":user_dict.get("sex", ),
        "age":user_dict.get("age", ),
        "org":user_dict.get("org", ),
        "year":user_dict.get("year", ),
        "spec":user_dict.get("spec", ),
        "class":user_dict.get("class", ),
        "region":region,
        "area":area,
        "build":build,
        "dorm":dorm,
        "mobile":mobile,
        "jt_mobile":homemobile,
        "province":user_dict.get("province", ),
        "city":user_dict.get("city", ),
        "district":user_dict.get("district", ),
        "address":user_dict.get("address", ),
        "hjdz":user_dict.get("hjdz", ),
        "hj_province":user_dict.get("hj_province", ),
        "hj_city":user_dict.get("hj_province", ),
        "hj_district":user_dict.get("hj_district", ),
        "out":"","out_address":"[]","hb":"","hb_area":"","hn":"","hn_area":"",
        "lat":lat,"lon":lon,
        "gcj_lat":lat,"gcj_lon":lon,
        "jz_address":gpslocation,
        "jz_province":"河南省",
        "jz_city":"郑州市", #禹州市
        "jz_district":"金水区",#高新区
        "jz_sfyz":"是",
        "sj_province":"",
        "sj_city":"",
        "sj_district":"",
        "temp":"正常",
        "jrzz":"无","jzqk":"","stzk":"无症状","jcbl":"","jcqk":"","yqgl":"否","glrq":"","gljc":"","glp":"","glc":"","gld":"","gla":"","glyy":"","yjs":0,"other":"","hb_date":"","jz_qzbl":"","tz_qzbl":"","tz_province":"","tz_city":"","tz_district":"","tz_area":"","tz_address":"","jc_yqjc":"","jc_jcrq":"","jc_province":"","jc_city":"","jc_district":"","jc_area":"","jc_address":"","qz_yqbl":"否","qz_yqrq":"","zl_province":"","zl_city":"","zl_district":"","zl_area":"","zl_address":"","zl_sfzy":"","zl_zyrq":"","xq_province":"","xq_city":"","xq_district":"","xq_area":"","xq_address":"","home_time":"","wj_type":1
    }
    
    dormdata={"user_code":user_dict.get("user_code", ),
        "user_name":user_dict.get("user_name", ),
        "id_card":user_dict.get("id_card", ),
        "date":datetime,"sex":user_dict.get("sex", ),
        "age":user_dict.get("age", ),
        "org":user_dict.get("org", ),
        "year":user_dict.get("year", ),
        "spec":user_dict.get("spec", ),
        "class":user_dict.get("class", ),
        "region":region,
        "area":area,
        "build":build,
        "dorm":dorm,
        "mobile":mobile,
        "jt_mobile":homemobile,
        "province":user_dict.get("province", ),
        "city":user_dict.get("city", ),
        "district":user_dict.get("district", ),
        "address":user_dict.get("address", ),
        "hjdz":user_dict.get("hjdz", ),
        "hj_province":user_dict.get("hj_province", ),
        "hj_city":user_dict.get("hj_province", ),
        "hj_district":user_dict.get("hj_district", ),
        "out":"","out_address":"[]","hb":"","hb_area":"","hn":"","hn_area":"",
        "lat":lat,"lon":lon,
        "gcj_lat":lat,"gcj_lon":lon,
        "jz_address":gpslocation,
        "jz_province":"河南省",
        "jz_city":"郑州市", #禹州市
        "jz_district":"金水区",#高新区
        "jz_sfyz":"是",
        "sj_province":"",
        "sj_city":"",
        "sj_district":"",
        "temp":"正常",
        "jrzz":"无","jzqk":"","stzk":"无症状","jcbl":"","jcqk":"","yqgl":"否","glrq":"","gljc":"","glp":"","glc":"","gld":"","gla":"","glyy":"","yjs":0,"other":"","hb_date":"","jz_qzbl":"","tz_qzbl":"","tz_province":"","tz_city":"","tz_district":"","tz_area":"","tz_address":"","jc_yqjc":"","jc_jcrq":"","jc_province":"","jc_city":"","jc_district":"","jc_area":"","jc_address":"","qz_yqbl":"否","qz_yqrq":"","zl_province":"","zl_city":"","zl_district":"","zl_area":"","zl_address":"","zl_sfzy":"","zl_zyrq":"","xq_province":"","xq_city":"","xq_district":"","xq_area":"","xq_address":"",
        "home_time":"20:00","wj_type":3}
    ###home_time默认20:00
    #####以下代码为post部分
    # 转换data字典类型为字符串类型并支持中文
    if reporttype=="home":
        datajson = json.dumps(homedata, ensure_ascii=False)
    elif reporttype == "morn":
        datajson = json.dumps(morndata, ensure_ascii=False)
    elif reporttype == "dorm":
        datajson = json.dumps(dormdata, ensure_ascii=False)
    #print(datajson)
    ##############data字典处理结束################
    ##############邮箱配置开始################

    #定义邮件函数

    ##############邮箱配置结束################
    ##############发送请求！！！################
    r=requests.post("http://msg.zzuli.edu.cn/xsc/add", data=datajson.encode(), cookies=cookies, headers=headers)

    driver.quit()
    if r.status_code ==200:
        return(1)
    else:
        return(0)
