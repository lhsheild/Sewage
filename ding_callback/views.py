import json

import requests
from django.shortcuts import HttpResponse

from lib import crypto
from conf import my_setting


'''常量'''
DINGTALK_CORP_ID = "ding064ce37e8c6fff8435c2f4657eb6378f"  # Target key
# 钉钉微应用
DINGTALK_APP_KEY = "dingmdy8p4txyehahwqv"
DINGTALK_CORP_SECRET = "msKp0WTSjbgcaLmhmBUJhYhqkpWua-Gu8HTvSxhTf1tgIwuf4U50a_CXqoQVzYQg"

# 钉钉aes加密(随机)
DINGTALK_AES_TOKEN = "1234567890123456789012345678901234567890123"
DINGTALK_TOKEN = '123456'


# Create your views here.
# 注册审批回调
def register_callback(request):
    # 获取access_token
    appkey = 'dingmdy8p4txyehahwqv'
    appsecret = 'msKp0WTSjbgcaLmhmBUJhYhqkpWua-Gu8HTvSxhTf1tgIwuf4U50a_CXqoQVzYQg'
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 注册回调事件
    data = {'call_back_tag': ['bpms_task_change', 'bpms_instance_change'], 'token': '123456',
            'aes_key': '1234567890123456789012345678901234567890123',
            'url': 'http://lh.vaiwan.com/get_bms_callback/'}
    data = json.dumps(data)
    reg = requests.post('https://oapi.dingtalk.com/call_back/register_call_back?access_token={}'.format(access_token),
                        data=data)
    # print('reg_json: ', reg.json())

    return HttpResponse('register')


# 处理审批回调
def get_bms_callback(request):
    aes_key = '1234567890123456789012345678901234567890123'
    key = DINGTALK_CORP_ID

    if request.method == 'POST':
        print('body:', request.body)
        if request.POST:
            print('POST:', request.POST)

        # 验证签名并解密
        path_info = request.GET
        signature = path_info.get('signature')
        timestamp = path_info.get('timestamp')
        nonce = path_info.get('nonce')
        # print('signature, timestamp, nonce ：', signature, ';', timestamp, ';', nonce)
        ret = request.body.decode('utf-8')
        ret = json.loads(ret)
        ret = ret.get('encrypt')
        if crypto.check_callback_signature('123456', ret, signature, timestamp, nonce):
            print('ret ：', crypto.decrypt(aes_key, ret))
            msg, key, buf = crypto.decrypt(aes_key, ret)
            if msg.get('EventType') == "check_url":
                # 加密SUCCESS,完成回调注册
                # ret_msg = crypto.encrypt_text(aes_key, 'success').decode('utf-8')
                ret_msg = crypto.encrypt(aes_key, 'success', key).decode('utf-8')
                sign = crypto.generate_callback_signature('123456', ret_msg, timestamp, nonce)
                # print('ret_msg：', type(ret_msg), ret_msg)
                ret_json = json.dumps(
                    {'msg_signature': sign, 'timeStamp': timestamp, 'nonce': nonce, 'encrypt': ret_msg})
                # print('ret_json：', ret_json)
            # 判断审批事件为结束，且审批意见为同意
            elif msg.get('EventType') == "bpms_instance_change" and msg.get('result') == 'agree' and msg.get('processCode') in my_setting.process_code_lst:
                # todo，先设计数据库结构
                pass
            print('msg : ', msg)
            print('key : ', msg)
            print('buf : ', buf)
        return HttpResponse(ret_json)
    else:
        print('GET:', request.GET)
        return HttpResponse('2')


def get_failed_callback(request):
    # 获取access_token
    appkey = 'dingmdy8p4txyehahwqv'
    appsecret = 'msKp0WTSjbgcaLmhmBUJhYhqkpWua-Gu8HTvSxhTf1tgIwuf4U50a_CXqoQVzYQg'
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 获取失败回调
    url = 'https://oapi.dingtalk.com/call_back/get_call_back_failed_result?access_token={}'.format(access_token)
    get_info = requests.get(url)
    # 失败列表
    failed_list = get_info.json().get('failed_list')
    if failed_list:
        for i in failed_list:
            print(i)
    return HttpResponse('获取失败回调')


def check_callback_api(request):
    # 获取access_token
    appkey = 'dingmdy8p4txyehahwqv'
    appsecret = 'msKp0WTSjbgcaLmhmBUJhYhqkpWua-Gu8HTvSxhTf1tgIwuf4U50a_CXqoQVzYQg'
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 查询回调接口
    url = 'https://oapi.dingtalk.com/call_back/get_call_back?access_token={}'.format(access_token)
    get_info = requests.get(url).json()
    print(get_info)
    return HttpResponse('查询回调接口')


def update_callback_api(request):
    # 获取access_token
    appkey = 'dingmdy8p4txyehahwqv'
    appsecret = 'msKp0WTSjbgcaLmhmBUJhYhqkpWua-Gu8HTvSxhTf1tgIwuf4U50a_CXqoQVzYQg'
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 更新回调接口
    url = 'https://oapi.dingtalk.com/call_back/update_call_back?access_token={}'.format(access_token)
    data = {'call_back_tag': ['bpms_task_change', 'bpms_instance_change'],
            'token': '123456',
            'aes_key': '1234567890123456789012345678901234567890123',
            'url': 'http://lh.vaiwan.com/get_bms_callback/'}
    data = json.dumps(data)
    get_info = requests.post(url, data=data).json()
    print(get_info)
    return HttpResponse('更新回调接口')
