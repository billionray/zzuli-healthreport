import requests
from requests_html import HTMLSession
import json
import base64
from .data import data_generate

# 常量
url = "http://kys.zzuli.edu.cn/cas/login"
getHeader = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "onnection": "keep-alive",
    "Host": "kys.zzuli.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.18 Safari/537.36"
} 
postHeader={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "141",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "kys.zzuli.edu.cn",
    "Origin": "http://kys.zzuli.edu.cn",
    "Referer": "http://kys.zzuli.edu.cn/cas/login",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.18 Safari/537.36"
}
session=HTMLSession()
base64Pwd = base64.b64encode(password.encode('utf-8')).decode('utf-8')
# 在登录前进行get，获取html和cookie
getResponse = session.get(url, headers = getHeader)
postCookie = getResponse.cookies

# 获取请求体中的lt和execution 
# TODO:加上判空条件 
lt = getResponse.html.find("[name=lt]") 
execution = getResponse.html.find("[name=execution]")

# 拼接请求体 并发送post请求获取cookie
payload = "username="+username+"&password={base64}_"+base64Pwd+"&secret=&lt="+lt[0].attrs["value"]+"&execution="+execution[0].attrs["value"]+"&_eventId=submit"
postResponse = session.post(url=url, headers=postHeader, cookies=postCookie, data=payload)
userCookie = postResponse.cookies
userHeader = postResponse.headers

