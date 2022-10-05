import time

import requests
from retrying import retry
from selenium import webdriver

from .data import data_generate
from .header import header_generate

proxies = {"http": None, "https": None}  # 代理
debug = 0  # 调试模式
'''
this module is the main module. it will get cookies and post your report data
if you are not developer,you must NOT write anything in this file
'''


@retry(stop_max_attempt_number=5, wait_fixed=10000)
def service(username, password, datetime, report_type, data):
    loginurl = "http://kys.zzuli.edu.cn/cas/login"
    url2 = "https://msg.zzuli.edu.cn/xsc/view?from=h5"

    # 创建浏览器对象
    try:
        if debug == 0:
            opt = webdriver.ChromeOptions()
            opt.add_argument('headless')
            opt.add_argument('no-sandbox')
            opt.add_argument('disable-dev-shm-usage')
            driver = webdriver.Chrome(options=opt)
        else:
            opt = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=opt)
    except:
        print("浏览器创建失败，请检查chromedriver配置")
        return 0

    # 执行登录命令
    driver.get(loginurl)
    time.sleep(0.1)
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
    driver.get(url2)
    link = driver.find_elements_by_xpath("//*[@data-href]")[0]  # 获取打卡页的链接

    # 处理每日打卡链接
    dakaurl = link.get_attribute('data-href')
    getuserurl = dakaurl.replace('view?from=h5&', 'get_user_info?') + "&wj_type=0"  # 截取从学校服务器储存的data
    if report_type == "home":
        dakaurl = dakaurl + "&date=" + datetime
    elif report_type == "morn":
        dakaurl = dakaurl + "&date=" + datetime
        dakaurl = dakaurl.replace('xsc', 'morn')
        getuserurl = getuserurl.replace('&wj_type=0', '&wj_type=1')
    elif report_type == "dorm":
        dakaurl = dakaurl + "&date=" + datetime
        dakaurl = dakaurl.replace('xsc', 'dorm')
        getuserurl = getuserurl.replace('&wj_type=0', '&wj_type=3')

    finaldakaurl = dakaurl
    if debug == 1:
        print(f"从服务器获取的链接：\n{getuserurl}")
        print(f"打卡链接：\n{dakaurl}")

    # 得到cookie
    driver.get(finaldakaurl)
    time.sleep(0.5)

    # 处理弹框
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

    # 获取cookie
    cookies = {}
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']

    # 获取header
    headers = header_generate(finaldakaurl, cookies)

    if debug == 1:
        print(f"header处理的结果：\n{headers[1]}")

    data_json = data_generate(getuserurl, headers, cookies, proxies, debug, report_type, data, datetime)

    if debug == 1:
        print(f"生成的data：\n{data_json}")
    result = requests.post("http://msg.zzuli.edu.cn/xsc/add", data=data_json.encode(), cookies=cookies,
                           headers=headers[1], proxies=proxies)
    driver.quit()
    if result.status_code == 200:
        return 1
    else:
        return 0
