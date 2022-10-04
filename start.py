# 用于配制程序的自动更细
import os
import urllib.request
import zipfile
from shutil import copyfile, rmtree

from retrying import retry

# 是否使用国内节点
mirror = False


@retry(stop_max_attempt_number=3, wait_fixed=10000)
def update():
    if mirror:
        urllib.request.urlretrieve("http://daka_download.xwwwb.com/code.zip", "code.zip")
        zip_file = zipfile.ZipFile('code.zip')
        zip_file.extractall()
    else:
        os.system('git clone --depth 1 https://github.com/billionray/zzuli-healthreport.git code')


# 先下载到最新的代码
try:
    update()
except:
    print("拉取代码失败")

# 删除代码中的空的json
os.remove("./code/data.json")
# 拷贝有数据的data.json到code中
if os.path.exists('/.dockerenv'):
    copyfile("./config/data.json", "./code/data.json")
else:
    copyfile("./data.json", "./code/data.json")

os.system("cd code && python3 run.py")

rmtree("./code")

if mirror:
    os.remove("code.zip")
