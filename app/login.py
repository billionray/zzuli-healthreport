import requests
from requests_html import HTMLSession
import json
import base64

username = "填入账号"
password = '填入密码'
binPwd = password.encode('utf-8')
base64Pwd = base64.b64encode(binPwd).decode('utf-8')
session=HTMLSession()
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

url = "http://kys.zzuli.edu.cn/cas/login"
getResponse = session.get(url, headers = getHeader)
postCookie = getResponse.cookies
print(postCookie)
lt = getResponse.html.find("[name=lt]")
execution = getResponse.html.find("[name=execution]")
print()
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
data = "username="+username+"&password={base64}_"+base64Pwd+"&secret=&lt="+lt[0].attrs["value"]+"&execution="+execution[0].attrs["value"]+"&_eventId=submit"
print(data)

postResponse = session.post(url=url, headers=postHeader, cookies=postCookie, data=data)

userCookie = postResponse.cookies

print(userCookie)
