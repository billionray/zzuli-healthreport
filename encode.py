import base64
from Cryptodome.Cipher import AES #dependence:pycryptodomex
'''
this module is to get the report-history page code
the report-history page code is just make the sutdents' code encrypted by AES in local.
Personally I think it is not secure
'''
def encode(username): #username should be text

    def add_to_16(s): #if key is not 16 length,it will add 0 until it is 16 length
        while len(s) % 16 != 0:
            s += '\0'
        return str.encode(s)  # return bytes
     
     
    key ='1234567887654321'  # get from report page: https://msg.zzuli.edu.cn/xsc/view?from=h5&code= urcode
    text=username  # waiting for encoding
     
    aes = AES.new(str.encode(key), AES.MODE_ECB)  # initialize AES-ECB encrypt mode
    #the folloing code is suggested by visual studio to speed up the speed of runing
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    #decrypted_text = str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
    historyurl="https://msg.zzuli.edu.cn/xsc/log?type=0&code="+encrypted_text #synthesis the url
    finalhistoryurl=historyurl.replace('%2B', '+')
    return finalhistoryurl
