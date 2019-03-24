import requests
import os
import json
import datetime

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

    # monitors = models.MonitorPoint.objects.all()
    # for i in monitors:
    #     samples = i.sample.all()
    #     print(samples.values_list('sample_date', 'sample_time'))

    data = {'errcode': 0, 'process_instance': {'attached_process_instance_ids': [], 'biz_action': 'NONE',
                                               'business_id': '201903241350000261992',
                                               'cc_userids': ['2504294407695839'], 'create_time': '2019-03-24 13:50:27',
                                               'finish_time': '2019-03-24 13:50:33',
                                               'form_component_values': [{'name': '监测点', 'value': '1-4'},
                                                                         {'name': '监测点物探号', 'value': 'Uehegyxydu'}, {
                                                                             'ext_value': '当前时间:2019-03-24 13:49:57\n当前地点:广西壮族自治区南宁市青秀区南湖街道凤岭春天',
                                                                             'name': '["当前时间","当前地点"]',
                                                                             'value': '["2019-03-24 13:49:57",108.420996,22.81774,"广西壮族自治区南宁市青秀区南湖街道凤岭春天",30]'},
                                                                         {'name': '监测点外景照',
                                                                          'value': '["https://static.dingtalk.com/media/lADPBE1XX7WrjLrNBnTNBDg_1080_1652.jpg"]'},
                                                                         {'name': '监测点水流照',
                                                                          'value': '["https://static.dingtalk.com/media/lADPBE1XX7WrlSHNBnTNBDg_1080_1652.jpg"]'},
                                                                         {'name': '无法监测原因', 'value': '浪费时间'},
                                                                         {'name': '是否合格', 'value': '是'}],
                                               'operation_records': [
                                                   {'date': '2019-03-24 13:50:26', 'operation_result': 'NONE',
                                                    'operation_type': 'START_PROCESS_INSTANCE', 'userid': 'manager405'},
                                                   {'date': '2019-03-24 13:50:32', 'operation_result': 'AGREE',
                                                    'operation_type': 'EXECUTE_TASK_NORMAL', 'remark': '',
                                                    'userid': 'manager405'},
                                                   {'date': '2019-03-24 13:50:32', 'operation_result': 'NONE',
                                                    'operation_type': 'NONE', 'remark': '', 'userid': 'manager405'}],
                                               'originator_dept_id': '104659413', 'originator_dept_name': '水质组',
                                               'originator_userid': 'manager405', 'result': 'agree',
                                               'status': 'COMPLETED', 'tasks': [
            {'create_time': '2019-03-24 13:50:27', 'finish_time': '2019-03-24 13:50:33', 'task_result': 'AGREE',
             'task_status': 'COMPLETED', 'taskid': '60046304784', 'userid': 'manager405'}],
                                               'title': '梁昊提交的流量水质监测（无法监测）'}, 'request_id': '55s332ulkn67'}

    all_data = data.get('process_instance').get('form_component_values')

    not_monitor_reason = all_data[5].get('value')
    print(not_monitor_reason)
