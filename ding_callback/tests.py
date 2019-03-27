import requests
import os
import json
import datetime
import itertools

from conf import my_setting


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
    # time.sleep(2)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sewage.settings")
    import django

    django.setup()

    from ding_callback import models
    from lib.common import list_split

    data_dic = {'errcode': 0, 'process_instance': {'attached_process_instance_ids': [], 'biz_action': 'NONE',
                                                   'business_id': '201903271155000450270',
                                                   'cc_userids': ['2504294407695839'],
                                                   'create_time': '2019-03-27 11:55:45',
                                                   'finish_time': '2019-03-27 11:55:52',
                                                   'form_component_values': [{'name': '监测点', 'value': 'L1-3'},
                                                                             {'name': '监测点物探号', 'value': 'LHH'}, {
                                                                                 'ext_value': '当前时间:2019-03-27 11:55:15\n当前地点:广西壮族自治区南宁市青秀区 建政街道景都国际大酒店',
                                                                                 'name': '["当前时间","当前地点"]',
                                                                                 'value': '["2019-03-27 11:55:15",108.363395,22.825507,"广西 壮族自治区南宁市青秀区建政街道景都国际大酒店",29]'},
                                                                             {'name': '监测点外景照',
                                                                              'value': '["https://static.dingtalk.com/media/lADPBE1XX7y-Ky7NBnTNBDg_1080_1652.jpg"]'},
                                                                             {'name': '监测点水流照',
                                                                              'value': '["https://static.dingtalk.com/media/lADPBE1XX7y-S1DNBnTNBDg_1080_1652.jpg"]'},
                                                                             {'name': '无法监测原因', 'value': '浪费时间'},
                                                                             {'name': '是否合格', 'value': ' 是'}],
                                                   'operation_records': [
                                                       {'date': '2019-03-27 11:55:45', 'operation_result': 'NONE',
                                                        'operation_type': 'START_PROCESS_INSTANCE',
                                                        'userid': 'manager405'},
                                                       {'date': '2019-03-27 11:55:51', 'operation_result': 'AGREE',
                                                        'operation_type': 'EXECUTE_TASK_NORMAL', 'remark': '',
                                                        'userid': 'manager405'},
                                                       {'date': '2019-03-27 11:55:51', 'operation_result': 'NONE',
                                                        'operation_type': 'NONE', 'remark': '',
                                                        'userid': 'manager405'}], 'originator_dept_id': '104659413',
                                                   'originator_dept_name': '水质组', 'originator_userid': 'manager405',
                                                   'result': 'agree', 'status': 'COMPLETED', 'tasks': [
            {'create_time': '2019-03-27 11:55:45', 'finish_time': '2019-03-27 11:55:51', 'task_result': 'AGREE',
             'task_status': 'COMPLETED', 'taskid': '61010289327', 'userid': 'manager405'}],
                                                   'title': '梁昊提交的流量水质监测（无法监测）'}, 'request_id': '5dleal6xp72j'}

    obj = models.MonitorPoint.objects.filter(people='曾玄介').first()
    t = obj.people + '梁昊'
    print(t)

    people = data_dic.get('process_instance').get('title').split('提交')[0]  # 监测者/采样者
    print(people)