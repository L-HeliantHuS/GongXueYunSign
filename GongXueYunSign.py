# -*- coding: utf8 -*-
import sys

import requests
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from hashlib import md5

# 配置信息
phone = ""  # 手机号 必填
password = ""  # 密码 必填
desc = ""  # 签到文本
longitude = "117.072340"  # 经度 必填
latitude = "36.636680"  # 纬度 必填
country = ""
province = "山东省"  # 所在省 必填
city = "济南市"  # 所在市 必填
address = "历下区*********"  # 签到地点名 必填
stateType = sys.argv[1]  # START or END
stateDesp = "上班" if stateType == "START" else "下班"

loginUrl = "https://api.moguding.net:9000/session/user/v3/login"
planUrl = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
saveUrl = "https://api.moguding.net:9000/attendence/clock/v2/save"

this_user = {}
SERVER_KEY = ""  # Server酱推送KEY 非必填 填了可以推送消息确定是否打卡成功
AES_KEY = b"23DbtQHR2UMbH6mJ"  # AES加密用的KEY
salt = "3478cbbc33f84bd00d75d7dfa69e0daa"  # md5加密用的盐
aes_encrypt = AES.new(AES_KEY, AES.MODE_ECB)  # aes加密实例


def postUrl(url, headers, data):
    requests.packages.urllib3.disable_warnings()
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return resp.json()


# getToken 登录 获取Token
def getToken():
    data = {
        "t": aes_encrypt.encrypt(pad(str(int(time.time() * 1000)).encode(), 16)).hex(),
        "password": aes_encrypt.encrypt(pad(password.encode(), 16)).hex(),
        "loginType": "android",
        "phone": aes_encrypt.encrypt(pad(phone.encode(), 16)).hex()

    }

    resp = postUrl(loginUrl, data=data, headers={"Content-Type": "application/json; charset=UTF-8",
                                                 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36'})

    global this_user
    this_user = resp['data']
    return resp['data']['token']


# getPlanId 获取计划
def getPlanId(headers):
    data = {"roleKey": "student",
            "sign": md5((this_user['userId'] + "student" + salt).encode()).hexdigest()}
    resp = postUrl(planUrl, headers, data)

    return resp['data'][0]['planId']


# savePlan 签到
def savePlan(headers):
    data = {
        'device': 'android',
        'address': province + city + address,
        'description': desc,
        'country': country,
        'province': province,
        'city': city,
        'longitude': longitude,
        'latitude': latitude,
        'planId': getPlanId(headers),
        'type': stateType,
    }

    headers["sign"] = md5(("android" + stateType + data['planId'] + this_user['userId']
                           + province + city + address + salt).encode()).hexdigest()

    resp = postUrl(saveUrl, headers, data)
    return resp


# pushServer Server酱消息推送
def pushServer(t):
    if SERVER_KEY != "":
        requests.post(f"https://sc.ftqq.com/{SERVER_KEY}.send", data={
            "title": f"{stateDesp}打卡成功 {t}",
        })


# main 主函数
def main():
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
        'Authorization': getToken()
    }

    result = savePlan(headers)
    if result['code'] == 200:
        # Server酱通知
        pushServer(result['data']['createTime'])


if __name__ == '__main__':
    main()
