import json
import requests
import time
from selenium import webdriver
from retrying import retry

debug = 1  # 调试模式
'''
this module is the main module. it will get cookies and post your report data
if you are not developer,you must NOT write anything in this file
'''
@retry(stop_max_attempt_number=5,wait_fixed=10000)
def service(username, password, mobile, homemobile, gpslocation, lat, lon, datetime, reporttype, region, area, build,
            dorm, schoolgps, schoollat, schoollon):
    #############################
    #  登录模块                   #
    #############################
    loginurl = "http://kys.zzuli.edu.cn/cas/login"
    url2 = "https://msg.zzuli.edu.cn/xsc/view?from=h5"

    try:
        opt = webdriver.ChromeOptions()  # 创建浏览器
        opt.add_argument('headless')
        opt.add_argument('no-sandbox')
        opt.add_argument('disable-dev-shm-usage')
        driver = webdriver.Chrome(options=opt)  # create the browser
    except:
        print("浏览器创建失败，请检查chromedriver配置")
    driver.get(loginurl)
    # driver.maximize_window()                      #maximize the window
    time.sleep(0.1)  # 加载等待
    script_switch1 = '$(".loginSwitch img").click()'
    driver.execute_script(script_switch1)
    time.sleep(0.1)
    script_switch2 = '$(".changeBtn").click()'
    driver.execute_script(script_switch2)
    time.sleep(0.1)
    driver.find_element_by_id("username").send_keys(username)  # 输入账号
    driver.find_element_by_id("password").send_keys(password)  # 输入密码
    driver.execute_script("loginIdsAndCas1()")

    time.sleep(0.1)
    #############肺炎打卡##################
    #############################
    #  链接处理                   #
    #############################
    driver.get(url2)

    for link in driver.find_elements_by_xpath("//*[@data-href]"):  # 获取data-href元素

        # 处理每日打卡链接
        dakaurl = link.get_attribute('data-href')
        getuserurl = dakaurl  # 截取学校储存的data
        getuserurl = getuserurl.replace('view?from=h5&', 'get_user_info?') + "&wj_type=0"
        if reporttype == "home":
            dakaurl = dakaurl + "&date=" + datetime
        elif reporttype == "morn":
            dakaurl = dakaurl + "&date=" + datetime
            dakaurl = dakaurl.replace('xsc', 'morn')
            getuserurl = getuserurl.replace('&wj_type=0', '&wj_type=1')
        elif reporttype == "dorm":
            dakaurl = dakaurl + "&date=" + datetime
            dakaurl = dakaurl.replace('xsc', 'dorm')
            getuserurl = getuserurl.replace('&wj_type=0', '&wj_type=3')
        # 结束
        finaldakaurl = dakaurl + "&date=" + datetime
        if debug == 1:
            print(f"从服务器获取的链接：\n{getuserurl}")
            print(f"打卡链接：\n{dakaurl}")
        # get cookie
        driver.get(finaldakaurl)
        time.sleep(1)
        for i in range(0, 5):
            try:
                links = driver.find_elements_by_xpath("//a")
                break
            except Exception as e:
                if 'alert' in str(e):
                    pass
                else:
                    links = []
                    break
        selenium_cookies = driver.get_cookies()

    #############################
    #  cookie处理                #
    #############################

    cookies = {}
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']

    # 替换cookie中可能出现的%3D为等号
    xsrftoken = cookies.get("XSRF-TOKEN", )
    xxsrftoken = xsrftoken.replace('%3D', '=')
    get_headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "DNT": "1",
        "X-XSRF-TOKEN": xxsrftoken,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": ("%s" % finaldakaurl),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID=" + cookies["PHPSESSID"] + ";XSRF-TOKEN=" + cookies[
            "XSRF-TOKEN"] + ";" + "laravel_session=" + cookies["laravel_session"]
    }

    headers = {
        "Connection": "keep-alive",
        "X-XSRF-TOKEN": xxsrftoken,
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://msg.zzuli.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": ("%s" % finaldakaurl),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID=" + cookies["PHPSESSID"] + ";XSRF-TOKEN=" + cookies[
            "XSRF-TOKEN"] + ";" + "laravel_session=" + cookies["laravel_session"]
    }
    if debug == 1:
        print(f"header处理的结果：\n{headers}")
    #############################
    #  data处理                  #
    #############################

    sourcedata = requests.get(getuserurl, headers=get_headers, cookies=cookies)  # 获取服务器数据
    sourcedata.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
    yuandata = sourcedata.text
    user_dict = json.loads(yuandata)
    if debug == 1:
        print(f"从服务器获取的数据：\n{user_dict}")
    homedata = {
        "user_code": user_dict.get("user_code", ), "user_name": user_dict.get("user_name", ),
        "id_card": user_dict.get("id_card", ), "date": datetime, "sex": user_dict.get("sex", ),
        "age": user_dict.get("age", ), "org": user_dict.get("org", ), "year": user_dict.get("year", ),
        "spec": user_dict.get("spec", ), "class": user_dict.get("class", ), "region": "", "area": "",
        "build": "", "dorm": "", "mobile": mobile, "jt_mobile": homemobile, "province": user_dict.get("province", ),
        "city": user_dict.get("city", ),
        "district": user_dict.get("district", ), "address": user_dict.get("address", ), "hjdz": user_dict.get("hjdz", ),
        "hj_province": user_dict.get("hj_province", ), "hj_city": user_dict.get("hj_city", ),
        "hj_district": user_dict.get("hj_district", ),
        "out": "否",
        "out_address": "[{\"start_date\":\"\",\"end_date\":\"\",\"province\":\"\",\"city\":\"\",\"district\":\"\",\"area\":\"\",\"address\":\"\"}]",
        "hb": "否", "hb_area": "", "hn": "否", "hn_area": "", "lat": lat, "lon": lon, "gcj_lat": lat,
        "gcj_lon": lon, "jz_address": gpslocation, "jz_province": user_dict.get("province", ),
        "jz_city": user_dict.get("city", ),
        "jz_district": user_dict.get("district", ), "jz_sfyz": "是", "sj_province": "", "sj_city": "", "sj_district": "",
        "temp": "正常",
        "jrzz": "无", "jzqk": "", "stzk": "无症状", "jcbl": "否", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "", "glp": "",
        "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "无", "hb_date": "", "jz_qzbl": "",
        "tz_qzbl": "",
        "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "",
        "jc_jcrq": "",
        "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "", "qz_yqbl": "否",
        "qz_yqrq": "",
        "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "", "zl_address": "", "zl_sfzy": "",
        "zl_zyrq": "",
        "xq_province": "", "xq_city": "", "xq_district": "", "xq_area": "", "xq_address": "", "home_time": "",
        "wj_type": 0
    }
    morndata = {
        "user_code": user_dict.get("user_code", ),
        "user_name": user_dict.get("user_name", ),
        "id_card": user_dict.get("id_card", ),
        "date": datetime, "sex": user_dict.get("sex", ),
        "age": user_dict.get("age", ),
        "org": user_dict.get("org", ),
        "year": user_dict.get("year", ),
        "spec": user_dict.get("spec", ),
        "class": user_dict.get("class", ),
        "region": region,
        "area": area,
        "build": build,
        "dorm": dorm,
        "mobile": mobile,
        "jt_mobile": homemobile,
        "province": user_dict.get("province", ),
        "city": user_dict.get("city", ),
        "district": user_dict.get("district", ),
        "address": user_dict.get("address", ),
        "hjdz": user_dict.get("hjdz", ),
        "hj_province": user_dict.get("hj_province", ),
        "hj_city": user_dict.get("hj_province", ),
        "hj_district": user_dict.get("hj_district", ),
        "out": "", "out_address": "[]", "hb": "", "hb_area": "", "hn": "", "hn_area": "",
        "lat": schoollat, "lon": schoollon,
        "gcj_lat": schoollat, "gcj_lon": schoollon,
        "jz_address": schoolgps,
        "jz_province": user_dict.get("province", ),
        "jz_city": user_dict.get("city", ),
        "jz_district": user_dict.get("district", ),
        "jz_sfyz": "是",
        "sj_province": "",
        "sj_city": "",
        "sj_district": "",
        "temp": "正常",
        "jrzz": "无", "jzqk": "", "stzk": "无症状", "jcbl": "", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "", "glp": "",
        "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "无", "hb_date": "", "jz_qzbl": "",
        "tz_qzbl": "",
        "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "",
        "jc_jcrq": "", "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "",
        "qz_yqbl": "否", "qz_yqrq": "", "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "",
        "zl_address": "", "zl_sfzy": "", "zl_zyrq": "", "xq_province": "", "xq_city": "", "xq_district": "",
        "xq_area": "", "xq_address": "", "home_time": "", "wj_type": 1
    }

    dormdata = {"user_code": user_dict.get("user_code", ),
                "user_name": user_dict.get("user_name", ),
                "id_card": user_dict.get("id_card", ),
                "date": datetime, "sex": user_dict.get("sex", ),
                "age": user_dict.get("age", ),
                "org": user_dict.get("org", ),
                "year": user_dict.get("year", ),
                "spec": user_dict.get("spec", ),
                "class": user_dict.get("class", ),
                "region": region,
                "area": area,
                "build": build,
                "dorm": dorm,
                "mobile": mobile,
                "jt_mobile": homemobile,
                "province": user_dict.get("province", ),
                "city": user_dict.get("city", ),
                "district": user_dict.get("district", ),
                "address": user_dict.get("address", ),
                "hjdz": user_dict.get("hjdz", ),
                "hj_province": user_dict.get("hj_province", ),
                "hj_city": user_dict.get("hj_province", ),
                "hj_district": user_dict.get("hj_district", ),
                "out": "", "out_address": "[]", "hb": "", "hb_area": "", "hn": "", "hn_area": "",
                "lat": schoollat, "lon": schoollon,
                "gcj_lat": schoollat, "gcj_lon": schoollon,
                "jz_address": schoolgps,
                "jz_province": user_dict.get("province", ),
                "jz_city": user_dict.get("city", ),
                "jz_district": user_dict.get("district", ),
                "jz_sfyz": "是",
                "sj_province": "",
                "sj_city": "",
                "sj_district": "",
                "temp": "正常",
                "jrzz": "无", "jzqk": "", "stzk": "无症状", "jcbl": "", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "",
                "glp": "", "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "无", "hb_date": "",
                "jz_qzbl": "", "tz_qzbl": "", "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "",
                "tz_address": "", "jc_yqjc": "", "jc_jcrq": "", "jc_province": "", "jc_city": "", "jc_district": "",
                "jc_area": "", "jc_address": "", "qz_yqbl": "否", "qz_yqrq": "", "zl_province": "", "zl_city": "",
                "zl_district": "", "zl_area": "", "zl_address": "", "zl_sfzy": "", "zl_zyrq": "", "xq_province": "",
                "xq_city": "", "xq_district": "", "xq_area": "", "xq_address": "",
                "home_time": "20:00", "wj_type": 3}

    #############################
    #  data处理                  #
    #############################

    # 转换data字典类型为字符串类型并支持中文
    if reporttype == "home":
        datajson = json.dumps(homedata, ensure_ascii=False)
    elif reporttype == "morn":
        datajson = json.dumps(morndata, ensure_ascii=False)
    elif reporttype == "dorm":
        datajson = json.dumps(dormdata, ensure_ascii=False)

    if debug == 1:
        print(f"生成的data：\n{datajson}")
    r = requests.post("http://msg.zzuli.edu.cn/xsc/add", data=datajson.encode(), cookies=cookies, headers=headers)
    driver.quit()
    if r.status_code == 200:
        return (1)
    else:
        return (0)
