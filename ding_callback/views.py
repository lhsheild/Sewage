import json
from sys import modules
import os
import urllib
import datetime
import logging

bmps_logger = logging.getLogger('bmps_callback')

import requests
from django.shortcuts import HttpResponse

from lib import crypto, thread
from conf import my_setting
from ding_callback import models as ding_models


# Create your views here.
# 注册审批回调
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
def get_bms_callback(request):
    aes_key = my_setting.aes_key
    key = my_setting.corp_id

    if request.method == 'POST':
        # print('body:', request.body)
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
        if crypto.check_callback_signature(my_setting.token, ret, signature, timestamp, nonce):
            # print('ret ：', crypto.decrypt(aes_key, ret))
            msg, key, buf = crypto.decrypt(aes_key, ret)
            msg = json.loads(msg)
            if msg.get('EventType') == "check_url":
                # 加密SUCCESS,完成回调注册
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
                bpms_id = msg.get('processInstanceId')
                bmps_logger.info('获取审批回调，实例ID为：{}'.format(bpms_id))
                bpms_code = msg.get('processCode')
                get_bpms_data_by_bpmsID(bpms_id, bpms_code)
                print('msg : ', msg)
                # print('key : ', msg)
                # print('buf : ', buf)
        return HttpResponse('执行回调数据同步')
    else:
        print('GET:', request.GET)
        return HttpResponse('2')


def get_failed_callback(request):
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
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
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 查询回调接口
    url = 'https://oapi.dingtalk.com/call_back/get_call_back?access_token={}'.format(access_token)
    get_info = requests.get(url).json()
    print(get_info)
    return HttpResponse('查询回调接口')


def update_callback_api(request):
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    # 更新回调接口
    url = 'https://oapi.dingtalk.com/call_back/update_call_back?access_token={}'.format(access_token)
    data = {'call_back_tag': ['bpms_task_change', 'bpms_instance_change'],
            'token': my_setting.token,
            'aes_key': my_setting.aes_key,
            'url': 'http://lh.vaiwan.com/get_bms_callback/'}
    data = json.dumps(data)
    get_info = requests.post(url, data=data).json()
    print(get_info)
    return HttpResponse('更新回调接口')


# 通过审批实例ID获取审批数据，再根据对应的审批类型入库
def get_bpms_data_by_bpmsID(id, code):
    # 获取access_token
    appkey = my_setting.app_key
    appsecret = my_setting.app_secret
    ret = requests.get('https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(appkey, appsecret))
    access_token = ret.json().get('access_token')

    url = 'https://oapi.dingtalk.com/topapi/processinstance/get?access_token={}'.format(access_token)
    data = requests.post(url, data={'process_instance_id': id})
    data = data.json()  # 字典
    print('data : ', type(data), data)
    if hasattr(modules[__name__], my_setting.process_code_dic[code]):
        this_func = getattr(modules[__name__], my_setting.process_code_dic[code])
        this_func(data)


# 处理容器法的回调
def func_container(data_dic):
    all_data = data_dic.get('process_instance').get('form_component_values')
    name = all_data[0].get('value')  # 监测点
    geophysical_point = all_data[1].get('value')  # 物探点号
    upload_time = json.loads(all_data[3].get('value'))[0]  # 审批提交时间
    year_s, mon_s, day_s = upload_time.split(' ')[0].split('-')  # 年月日
    date = datetime.datetime(int(year_s), int(mon_s), int(day_s)).date()  # 检测日期/采样日期
    is_monitor = 1  # 是否监测，1为监测
    not_monitor_reason = None  # 无法监测原因

    exterior_photo_link_lst = json.loads(all_data[3].get('value'))  # 钉钉回调的外景照链接
    if exterior_photo_link_lst is not None:
        down_ex_photo_thread_lst = []  # 存放下载外景照线程的列表
        exterior_photo_lst = []  # 下载后外景照链接的列表
        for counter, exterior_photo_link in enumerate(exterior_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'exterior', counter)
            t = thread.MyThread(target=save_img, args=(exterior_photo_link, img_name, upload_time))
            down_ex_photo_thread_lst.append(t)
            t.start()
        for t in down_ex_photo_thread_lst:
            t.join()
            exterior_photo_lst.append(t.get_result())
        exterior_photo = json.dumps(exterior_photo_lst)  # 外景照（JSON序列化后存入数据库）

    water_flow_photo_link_lst = json.loads(all_data[3].get('value'))  # 钉钉回调的水流照链接
    if water_flow_photo_link_lst is not None:
        down_wf_photo_thread_lst = []  # 存放下载水流照线程的列表
        water_flow_photo_lst = []  # 下载后水流照链接的列表
        for counter_water, water_flow_photo_link in enumerate(water_flow_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'water_flow', counter_water)
            t = thread.MyThread(target=save_img, args=(water_flow_photo_link, img_name, upload_time))
            down_wf_photo_thread_lst.append(t)
            t.start()
        for t in down_wf_photo_thread_lst:
            t.join()
            water_flow_photo_lst.append(t.get_result())
        water_flow_photo = json.dumps(water_flow_photo_lst)  # 水流照（JSON序列化后存入数据库）

    work_photo_link_lst = json.loads(all_data[3].get('value'))  # 钉钉回调的工作照链接
    if work_photo_link_lst is not None:
        down_work_photo_thread_lst = []  # 存放下载水流照线程的列表
        work_photo_lst = []  # 下载后水流照链接的列表
        for counter_work, work_photo_link in enumerate(work_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'work', counter_work)
            t = thread.MyThread(target=save_img, args=(work_photo_link, img_name, upload_time))
            down_work_photo_thread_lst.append(t)
            t.start()
        for t in down_work_photo_thread_lst:
            t.join()
            work_photo_lst.append(t.get_result())
        work_photo = json.dumps(work_photo_lst)  # 工作照（JSON序列化后存入数据库）

    people = data_dic.get('process_instance').get('title').split('提交')[0]  # 监测者/采样者

    monitor_time_str = all_data[6].get('value')
    hour_s, min_s = monitor_time_str.split(':')
    monitor_time = datetime.datetime(int(year_s), int(mon_s), int(day_s), int(hour_s), int(min_s)).time()  # 检测/采样时间段

    # 容器法测流量
    time1 = all_data[7].get('value')
    volume1 = all_data[8].get('value')
    time2 = all_data[9].get('value')
    volume2 = all_data[10].get('value')
    time3 = all_data[11].get('value')
    volume3 = all_data[12].get('value')

    # 样品编号
    sample_number = all_data[13].get('value')

    sample_photo_link_lst = json.loads(all_data[15].get('value'))  # 钉钉回调的样品照链接
    if sample_photo_link_lst is not None:
        down_sample_photo_thread_lst = []  # 存放下载样品照线程的列表
        sample_photo_lst = []  # 下载后样品照链接的列表
        for counter_sample, sample_photo_link in enumerate(sample_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'sample', counter_sample)
            t = thread.MyThread(target=save_img, args=(sample_photo_link, img_name, upload_time))
            down_sample_photo_thread_lst.append(t)
            t.start()
        for t in down_sample_photo_thread_lst:
            t.join()
            sample_photo_lst.append(t.get_result())
        sample_photo = json.dumps(sample_photo_lst)  # 样品照（JSON序列化后存入数据库）

    # 样品颜色
    sample_color = all_data[16].get('value')
    # 样品气味
    sample_odor = all_data[17].get('value')
    # 样品浊度
    sample_turbidity = all_data[18].get('value')


# 下载图片
def save_img(img_url, file_name, upload_time, file_path=my_setting.img_folder_path):
    year_s, mon_s, day_s = upload_time.split(' ')[0].split('-')
    save_path = '{}{}{}{}{}{}{}'.format(file_path, os.sep, year_s, os.sep, mon_s, os.sep, day_s)
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_suffix = os.path.splitext(img_url)[1]
        filename = '{}{}{}{}'.format(save_path, os.sep, file_name, file_suffix)
        urllib.urlretrieve(img_url, filename=filename)
        return filename
    except IOError as e:
        bmps_logger.error('{}：{}'.format(file_name, e))
    except Exception as e:
        bmps_logger.error('{}：{}'.format(file_name, e))
