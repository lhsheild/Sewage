from __future__ import absolute_import
from celery import shared_task
import requests
import json
import datetime
import urllib
import os
from sys import modules

from conf import my_setting


@shared_task
def add(x, y):
    return x + y


# 通过审批实例ID获取审批数据，再根据对应的审批类型入库
@shared_task
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
    else:
        print('没有对应审批流程回调处理方法！')


def func_container(data_dic):
    all_data = data_dic.get('process_instance').get('form_component_values')
    name = all_data[0].get('value')  # 监测点
    geophysical_point = all_data[1].get('value')  # 物探点号
    work_function = 0
    upload_time = json.loads(all_data[2].get('value'))[0]  # 审批提交时间
    year_s, mon_s, day_s = upload_time.split(' ')[0].split('-')  # 年月日
    date = datetime.datetime(int(year_s), int(mon_s), int(day_s)).date()  # 检测日期/采样日期
    file_path = my_setting.img_folder_path
    save_path = '{}{}{}{}{}{}{}'.format(file_path, os.sep, year_s, os.sep, mon_s, os.sep, day_s)

    exterior_photo_link_lst = json.loads(all_data[3].get('value'))  # 钉钉回调的外景照链接
    # if exterior_photo_link_lst is not None:
    #     exterior_photo = json.dumps(exterior_photo_link_lst)
    #     print(exterior_photo)
    if exterior_photo_link_lst is not None:
        exterior_photo_lst = []
        for counter, exterior_photo_link in enumerate(exterior_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'exterior', counter)
            img_path = save_img((exterior_photo_link, img_name, upload_time, my_setting.img_folder_path))
            exterior_photo_lst.append(img_path)
        exterior_photo = json.dumps(exterior_photo_lst)  # 外景照（JSON序列化后存入数据库）

    water_photo_link_lst = json.loads(all_data[4].get('value'))  # 钉钉回调的水流照链接
    # if water_photo_link_lst is not None:
    #     water_photo = json.dumps(water_photo_link_lst)
    #     print(water_photo)
    if water_photo_link_lst is not None:
        water_photo_lst = []
        for counter, water_photo_link in enumerate(water_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'water', counter)
            img_path = save_img((water_photo_link, img_name, upload_time, my_setting.img_folder_path))
            water_photo_lst.append(img_path)
        water_photo = json.dumps(water_photo_lst)

    work_photo_link_lst = json.loads(all_data[5].get('value'))  # 钉钉回调的工作照链接
    # if work_photo_link_lst is not None:
    #     work_photo = json.dumps(work_photo_link_lst)
    #     print(work_photo)
    if work_photo_link_lst is not None:
        work_photo_lst = []
        for counter, work_photo_link in enumerate(work_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, 'work', counter)
            img_path = save_img((work_photo_link, img_name, upload_time, my_setting.img_folder_path))
            work_photo_lst.append(img_path)
        water_photo = json.dumps(work_photo_lst)

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
        sample_photo = json.dumps(sample_photo_link_lst)
        print(sample_photo)

    # 样品颜色
    sample_color = all_data[16].get('value')
    # 样品气味
    sample_odor = all_data[17].get('value')
    # 样品浊度
    sample_turbidity = all_data[18].get('value')


@shared_task
def save_img(list):
    try:
        for i, j in enumerate(list):
            print(i, j)
            r = requests.get(j, stream=True)
            with open(str(i) + '.jpg', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            r.close()
            print("downloading picture succed!")

    except IOError as e:
        print(e)
    except Exception as e:
        print(e)
# def save_img(in_args):
#     img_url = in_args[0]
#     file_name = in_args[1]
#     upload_time = in_args[2]
#     file_path = in_args[3]  # my_setting.img_folder_path
#     year_s, mon_s, day_s = upload_time.split(' ')[0].split('-')
#     save_path = '{}{}{}{}{}{}{}'.format(file_path, os.sep, year_s, os.sep, mon_s, os.sep, day_s)
#     try:
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)
#             print(save_path)
#         file_suffix = os.path.splitext(img_url)[1]
#         filename = '{}{}{}{}'.format(save_path, os.sep, file_name, file_suffix)
#         # 下载方法1
#         urllib.request.urlretrieve(img_url, filename=filename)
#
#     except IOError as e:
#         print(e)
#     except Exception as e:
#         print(e)
