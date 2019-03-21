from __future__ import absolute_import
from celery import shared_task
import requests
import json
import datetime
import urllib
import os
from sys import modules

from conf import my_setting
from ding_callback import models


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
    print(name)
    geophysical_point = all_data[1].get('value')  # 物探点号
    print(geophysical_point)
    work_function = 0
    upload_time = json.loads(all_data[2].get('value'))[0]  # 审批提交时间
    year_s, mon_s, day_s = upload_time.split(' ')[0].split('-')  # 年月日
    date = datetime.datetime(int(year_s), int(mon_s), int(day_s)).date()  # 检测日期/采样日期
    print(date)
    file_path = my_setting.img_folder_path
    save_path = '{}{}{}{}{}{}{}'.format(file_path, os.sep, year_s, os.sep, mon_s, os.sep, day_s)

    exterior_photo_link_lst = json.loads(all_data[3].get('value'))  # 钉钉回调的外景照链接
    exterior_photo_lst = []
    if exterior_photo_link_lst is not None:
        for counter, exterior_photo_link in enumerate(exterior_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, '外景', counter)
            img_path = save_img((exterior_photo_link, img_name, upload_time, my_setting.img_folder_path))
            exterior_photo_lst.append(img_path)
    print(exterior_photo_lst)

    water_photo_link_lst = json.loads(all_data[4].get('value'))  # 钉钉回调的水流照链接
    water_photo_lst = []
    if water_photo_link_lst is not None:
        for counter, water_photo_link in enumerate(water_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, '水流', counter)
            img_path = save_img((water_photo_link, img_name, upload_time, my_setting.img_folder_path))
            water_photo_lst.append(img_path)
    print(water_photo_lst)

    work_photo_link_lst = json.loads(all_data[5].get('value'))  # 钉钉回调的工作照链接
    work_photo_lst = []
    if work_photo_link_lst is not None:
        for counter, work_photo_link in enumerate(work_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, '工作', counter)
            img_path = save_img((work_photo_link, img_name, upload_time, my_setting.img_folder_path))
            work_photo_lst.append(img_path)
    print(work_photo_lst)

    people = data_dic.get('process_instance').get('title').split('提交')[0]  # 监测者/采样者
    print(people)

    monitor_time_str = all_data[6].get('value')
    hour_s, min_s = monitor_time_str.split(':')
    monitor_time = datetime.datetime(int(year_s), int(mon_s), int(day_s), int(hour_s), int(min_s)).time()  # 检测/采样时间段
    print(monitor_time)

    # 容器法测流量
    time1 = all_data[7].get('value')
    print(time1)
    volume1 = all_data[8].get('value')
    print(volume1)
    time2 = all_data[9].get('value')
    print(time2)
    volume2 = all_data[10].get('value')
    print(volume2)
    time3 = all_data[11].get('value')
    print(time3)
    volume3 = all_data[12].get('value')
    print(volume3)

    # 样品编号
    sample_number = all_data[13].get('value')
    print(sample_number)

    sample_photo_link_lst = json.loads(all_data[15].get('value'))  # 钉钉回调的样品照链接
    sample_photo_lst = []
    if sample_photo_link_lst is not None:
        for counter, sample_photo_link in enumerate(sample_photo_link_lst):
            img_name = '{}_{}_{}'.format(name, '样品', counter)
            img_path = save_img((sample_photo_link, img_name, upload_time, my_setting.img_folder_path))
            sample_photo_lst.append(img_path)
    print(sample_photo_lst)

    # 样品颜色
    sample_color = all_data[16].get('value')
    print(sample_color)
    # 样品气味
    sample_odor = all_data[17].get('value')
    print(sample_odor)
    # 样品浊度
    sample_turbidity = all_data[18].get('value')
    print(sample_turbidity)

    try:
        from django.db import transaction
        with transaction.atomic():
            if models.MonitorPoint.objects.all().filter(geophysical_point=geophysical_point):
                monitor_obj = models.MonitorPoint.objects.all().filter(geophysical_point=geophysical_point).first()
                if exterior_photo_lst:
                    if monitor_obj.exterior_photo and json.dumps(json.loads(monitor_obj.exterior_photo)) is not 'null':
                        monitor_obj.exterior_photo = json.dumps(json.loads(monitor_obj.exterior_photo) + (exterior_photo_lst))
                    else:
                        monitor_obj.exterior_photo = json.dumps(exterior_photo_lst)
                if water_photo_lst:
                    if monitor_obj.water_flow_photo and json.dumps(json.loads(monitor_obj.water_flow_photo)) is not 'null':
                        monitor_obj.water_flow_photo = json.dumps(json.loads(monitor_obj.water_flow_photo) + (water_photo_lst))
                    else:
                        monitor_obj.water_flow_photo = json.dumps(water_photo_lst)
                if work_photo_lst:
                    if monitor_obj.work_photo and json.dumps(json.loads(monitor_obj.work_photo)) is not 'null':
                        monitor_obj.work_photo = json.dumps(json.loads(monitor_obj.work_photo) + (work_photo_lst))
                    else:
                        monitor_obj.work_photo = json.dumps(work_photo_lst)
                monitor_obj.save()
            else:
                monitor_obj = models.MonitorPoint.objects.create(
                    name=name,
                    geophysical_point=geophysical_point,
                    is_monitor=1,
                    work_function=0,
                    exterior_photo=json.dumps(exterior_photo_lst),
                    water_flow_photo=json.dumps(water_photo_lst),
                    work_photo=json.dumps(work_photo_lst)
                )
            print('MonitorPoint created!!')

            sample_dic = {
                'monitor_point': monitor_obj,
                'people': people,
                'sample_date': date,
                'sample_time': monitor_time,
                'sample_photo': json.dumps(sample_photo_lst),
                'sample_number': sample_number,
                'sample_color': sample_color,
                'sample_odor': sample_odor,
                'sample_turbidity': sample_turbidity
            }
            sample_obj = models.SampleInfo.objects.create(**sample_dic)
            print('SampleInfo created!!')

            flow_obj = models.FlowInfo.objects.create(
                monitor_point=monitor_obj,
                people=people,
                flow_date=date,
                flow_time=monitor_time,
                time1=time1,
                volume1=volume1,
                time2=time2,
                volume2=volume2,
                time3=time3,
                volume3=volume3
            )
            print('FlowInfo created!!')
    except Exception as e:
        print(e)


def save_img(in_args):
    img_url = in_args[0]
    file_name = in_args[1]
    upload_time = in_args[2]
    file_path = in_args[3]  # my_setting.img_folder_path
    year_s, mon_s, day_s = upload_time.split(' ')[0].split('-')
    save_path = '{}{}{}{}{}{}{}'.format(file_path, os.sep, year_s, os.sep, mon_s, os.sep, day_s)
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(save_path)
        file_suffix = os.path.splitext(img_url)[1]
        filename = '{}{}{}{}'.format(save_path, os.sep, file_name, file_suffix)
        # 下载方法1
        # urllib.request.urlretrieve(img_url, filename=filename)
        # 下载方法3
        r = requests.get(img_url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        r.close()
        return filename
        print("downloading picture succed!， {}".format(filename))

    except IOError as e:
        print(e)
    except Exception as e:
        print(e)
