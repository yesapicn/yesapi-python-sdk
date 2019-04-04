#!/usr/bin/python
#coding=utf-8
#
# 小白接口Python接入示例 - www.okayapi.com
#
# 执行前，需要有服务器上执行：
#
# yum install python-pip
# pip install requsts
#
# @author roy 20180131

import requests
import hashlib

# TODO: 请根据需要，换成您的HOST，app_key和app_secrect
API_URL     = 'http://api.okayapi.com/'
APP_KEY     = '16BD4337FB1D355902E0502AFCBFD4DF'
APP_SECRET  = '4c1402596e4cd017eeaO670df6f8B6783475b4ac8A32B4900f20abP2159711ad'

# 生成签名
def Signature(params, key=None, secret=None):
    key = key or APP_KEY
    secret = secret or APP_SECRET
    params.pop('app_secrect', None)
    params['app_key'] = key
    md5_ctx = hashlib.md5()
    md5_ctx.update(str(''.join([params[value] for value in sorted([key for key in params])]) + secret).encode('utf-8'))
    return md5_ctx.hexdigest().upper()
    

# 请求小白接口
def HTTPGet(url, params):
    params['sign'] = Signature(params)
    resp = requests.get(url, params)
    return resp.json()


def main():
    # 待请求的接口与相关参数
    params = {'s': 'Hello.World', 'name': 'dogstar'}

    # 发起请求
    return HTTPGet(API_URL, params)


print(main())
