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


CASTGC=postResponse.cookies['CASTGC']
JSESSIONID=getResponse.cookies['JSESSIONID']
client=getResponse.cookies['client']
#userHeader = postResponse.headers
print(postCookie)
#print(userHeader)
getDakaCookie=userCookie
print(getDakaCookie)
getDakaHeader={
"Host":"msg.zzuli.edu.cn",
"Connection": "keep-alive",
"DNT": "1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "none",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,zh-HK;q=0.6",
"Cache-Control": "max-age=0",
"Cookie":"CASTGC="+CASTGC+";JSESSIONID="+JSESSIONID+";client="+client
}
getDakaUrl="http://kys.zzuli.edu.cn/cas/login?service=http%3A%2F%2Fmsg.zzuli.edu.cn%2Fcas%2F%3F"
#getDakaUrl="http://kys.zzuli.edu.cn/cas/login?service=http%3A%2F%2Fmsg.zzuli.edu.cn%2Fcas%2F%3Ftz%3Dhttp%253A%252F%252Fmsg.zzuli.edu.cn%252Fxsc%252Fview%253Ffrom%253Dh5"
#getDakaUrl="https://msg.zzuli.edu.cn/cas/?tz=https%3A%2F%2Fmsg.zzuli.edu.cn%2Fxsc%2Fview%3Ffrom%3Dh5 "
getDakaResponse = requests.get(getDakaUrl, headers = getDakaHeader,verify=False,allow_redirects=True)
#print(getDakaResponse)
print(getDakaResponse.status_code)
print(getDakaResponse.url)

getMsgUrl=getDakaResponse.url
##提取PHPSESSID
PHPSESSID=getMsgUrl.split('ticket=')
PHPSESSID=PHPSESSID[1]
print(PHPSESSID)
##PHPSESSID
#getMsgUrl="http://msg.zzuli.edu.cn/cas/?tz=https%3A%2F%2Fmsg.zzuli.edu.cn%2Fxsc%2Fview%3Ffrom%3Dh5&ticket="+PHPSESSID
getMsgUrl="https://msg.zzuli.edu.cn/cas/?&ticket="+PHPSESSID
getMsgHeader={
"Host":"msg.zzuli.edu.cn",
"Connection": "keep-alive",
"DNT": "1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "none",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,zh-HK;q=0.6",
"Cache-Control": "max-age=0",
"Cookie":"PHPSESSID="+PHPSESSID
}
getMsgResponse = requests.get(getMsgUrl, headers = getMsgHeader,verify=False,allow_redirects=True)
finalurl=getMsgResponse.url
print(getDakaResponse.headers)
print(finalurl)
#reditList=getDakaResponse.history
#print(f'获取重定向的历史记录：{reditList}')
#print(f'获取第一次重定向的headers头部信息：{reditList[0].headers}')
#print(f'获取重定向最终的url：{reditList[len(reditList)-1].headers["location"]}')
