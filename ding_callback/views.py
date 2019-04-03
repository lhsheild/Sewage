import json
import logging

import requests

from ding_callback.tasks import get_bpms_data_by_bpmsID

logger = logging.getLogger('sewage views')

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

from lib import crypto
from conf import my_setting


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 注册审批回调
@csrf_exempt
def register_callback(request):
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 注册回调事件
    data = {'call_back_tag': ['bpms_task_change', 'bpms_instance_change'], 'token': my_setting.token,
            'aes_key': my_setting.aes_key,
            'url': 'http://lh.vaiwan.com/get_bms_callback/'}
    data = json.dumps(data)
    reg = requests.post('https://oapi.dingtalk.com/call_back/register_call_back?access_token={}'.format(access_token),
                        data=data)
    # print('reg_json: ', reg.json())
    return HttpResponse('register')


# 处理审批回调
@csrf_exempt
def get_bms_callback(request):
    aes_key = my_setting.aes_key
    key = my_setting.corp_id

    if request.method == 'POST':
        if request.POST:
            print('POST:', request.POST)

        # 验证签名并解密
        path_info = request.GET
        signature = path_info.get('signature')
        timestamp = path_info.get('timestamp')
        nonce = path_info.get('nonce')
        ret = request.body.decode('utf-8')
        ret = json.loads(ret)
        ret = ret.get('encrypt')
        if crypto.check_callback_signature(my_setting.token, ret, signature, timestamp, nonce):
            msg, key, buf = crypto.decrypt(aes_key, ret)
            msg = json.loads(msg)
            print(msg)

            # 加密SUCCESS,完成回调注册
            if msg.get('EventType') == "check_url":
                # ret_msg = crypto.encrypt_text(aes_key, 'success').decode('utf-8')
                ret_msg = crypto.encrypt(aes_key, 'success', key).decode('utf-8')
                sign = crypto.generate_callback_signature(my_setting.token, ret_msg, timestamp, nonce)
                # print('ret_msg：', type(ret_msg), ret_msg)
                ret_json = json.dumps(
                    {'msg_signature': sign, 'timeStamp': timestamp, 'nonce': nonce, 'encrypt': ret_msg})
                # print('ret_json：', ret_json)
                return HttpResponse(ret_json)

            # 判断审批事件为结束，且审批意见为同意
            elif msg.get('EventType') == "bpms_instance_change" and msg.get('result') == 'agree' and msg.get(
                    'processCode') in my_setting.process_code_lst:
                # 获取审批实例ID
                bpms_id = msg.get('processInstanceId')
                # bmps_logger.info('获取审批回调，实例ID为：{}'.format(bpms_id))
                bpms_code = msg.get('processCode')
                c_task = get_bpms_data_by_bpmsID.delay(bpms_id, bpms_code)
                c_task_id = c_task.id
                print("start running task：{}".format(c_task_id))
    else:
        print('GET:', request.GET)

    return HttpResponse(None)


@csrf_exempt
def get_failed_callback(request):
    info_lst = []
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    while True:
        # 获取失败回调
        url = 'https://oapi.dingtalk.com/call_back/get_call_back_failed_result?access_token={}'.format(access_token)
        get_info = requests.get(url).json()
        info_lst.append(get_info)
        # 失败列表
        failed_list = get_info.get('failed_list')
        if failed_list:
            for i in failed_list:
                print(i)
        if not get_info.get('has_more'):
            print('没有更多回调')
            break
    info_lst = json.dumps(info_lst)
    return HttpResponse(info_lst)


@csrf_exempt
def check_callback_api(request):
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 查询回调接口
    url = 'https://oapi.dingtalk.com/call_back/get_call_back?access_token={}'.format(access_token)
    get_info = requests.get(url).json()
    callback_url = get_info.get('url')
    callback_tag = get_info.get('call_back_tag')
    return render(request, 'callback.html', {'callback_url': callback_url, 'callback_tag': callback_tag})


@csrf_exempt
def update_callback_api(request):
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 更新回调接口
    url = 'https://oapi.dingtalk.com/call_back/update_call_back?access_token={}'.format(access_token)
    data = {'call_back_tag': ['bpms_instance_change'],
            'token': my_setting.token,
            'aes_key': my_setting.aes_key,
            'url': 'http://lh.vaiwan.com/get_bms_callback/'}
    data = json.dumps(data)
    get_info = requests.post(url, data=data).json()
    print(get_info)
    return HttpResponse('更新回调接口')
