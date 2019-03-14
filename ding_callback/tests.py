from django.test import TestCase
import sys
import os
import json
import datetime

# Create your tests here.
upload_time = json.loads(data.get('process_instance').get('form_component_values')[3].get('value'))[0]
data = {'errcode': 0, 'process_instance': {'attached_process_instance_ids': [], 'biz_action': 'NONE',
                                           'business_id': '201903142026000439544', 'cc_userids': ['2504294407695839'],
                                           'create_time': '2019-03-14 20:26:44', 'finish_time': '2019-03-14 20:26:51',
                                           'form_component_values': [{'name': '监测点', 'value': '测试'},
                                                                     {'name': '监测点物探号', 'value': '测试'},
                                                                     {
                                                                         'ext_value': '当前时间:2019-03-14 20:26:42\n当前地点:广西壮族自治区南宁市青秀区南湖街道凤岭春天',
                                                                         'name': '["当前时间","当前地点"]',
                                                                         'value': '["2019-03-14 20:26:42",108.421064,22.817492,"广西壮族自治区南宁市青秀区南湖街道凤岭春天",30]'},
                                                                     {'name': '监测点外景照',
                                                                      'value': '["https://static.dingtalk.com/media/lADPBE1XX57MOe7NBnTNBDg_1080_1652.jpg"]'},
                                                                     {'name': '监测点水流照',
                                                                      'value': '["https://static.dingtalk.com/media/lADPBE1XX57MSSjNBnTNBDg_1080_1652.jpg","https://static.dingtalk.com/media/lADPBE1XX59Fj0bNBnTNBDg_1080_1652.jpg"]'},
                                                                     {'name': '监测点工作照',
                                                                      'value': '["https://static.dingtalk.com/media/lADPBE1XX6AMnrrNBnTNBDg_1080_1652.jpg"]'},
                                                                     {'name': '检测时间段', 'value': '12:30'},
                                                                     {'name': '第一次检测时长', 'value': '33'},
                                                                     {'name': '第一次检测水量', 'value': '333'},
                                                                     {'name': '第二次检测时长', 'value': '333'},
                                                                     {'name': '第二次检测水量', 'value': '223'},
                                                                     {'name': '第三次检测时长', 'value': '222'},
                                                                     {'name': '第三次检测水量', 'value': '555'},
                                                                     {'name': '样品编号', 'value': '555'}, {'name': '检测指标',
                                                                                                        'value': '["COD NH3-N TP TN","BOD","溶氧量"]'},
                                                                     {'name': '样品照片',
                                                                      'value': '["https://static.dingtalk.com/media/lADPBE1XX57MPFPNBnTNBDg_1080_1652.jpg"]'},
                                                                     {'name': '颜色', 'value': '灰色'},
                                                                     {'name': '气味', 'value': '无味'},
                                                                     {'name': '浑浊度', 'value': '透明'},
                                                                     {'name': '是否合格', 'value': '是'}],
                                           'operation_records': [
                                               {'date': '2019-03-14 20:26:43', 'operation_result': 'NONE',
                                                'operation_type': 'START_PROCESS_INSTANCE', 'userid': 'manager405'},
                                               {'date': '2019-03-14 20:26:50', 'operation_result': 'AGREE',
                                                'operation_type': 'EXECUTE_TASK_NORMAL', 'remark': '',
                                                'userid': 'manager405'},
                                               {'date': '2019-03-14 20:26:50', 'operation_result': 'NONE',
                                                'operation_type': 'NONE', 'remark': '', 'userid': 'manager405'}],
                                           'originator_dept_id': '104659413', 'originator_dept_name': '水质组',
                                           'originator_userid': 'manager405', 'result': 'agree', 'status': 'COMPLETED',
                                           'tasks': [{'create_time': '2019-03-14 20:26:44',
                                                      'finish_time': '2019-03-14 20:26:51', 'task_result': 'AGREE',
                                                      'task_status': 'COMPLETED', 'taskid': '54281029278',
                                                      'userid': 'manager405'}], 'title': '梁昊提交的流量水质监测（容器法）'},
        'request_id': 'z24msfmr2xjb'}


def fun_container():
    print('容器法')


def fun_circle():
    print('圆管')


if __name__ == '__main__':
    # 容器法
    process_code_container = 'PROC-ELYJ1A4W-7WJ39FFR3417CDU1EEOZ2-D8YFWXSJ-2'
    # 流速法-圆管
    process_code_circle = 'PROC-0KYJJ30V-NXJ3PSN611HAPDGJ4UHZ1-9OW5YXSJ-5'
    # 流速法-方渠
    process_code_square = 'PROC-JFYJ09RV-68J3QPEB5YVCH8A5I0GM2-I01DYXSJ-L'
    # 仪器法
    process_code_machine = 'PROC-FFYJ5P8V-AYJ3732800LIXDXMYTIA3-ZU1GYXSJ-2'
    # 无法监测
    process_code_unable = 'PROC-ELYJ1A4W-SXJ37TP95QVKM4F1BV143-L84IYXSJ-4'

    # 需要回调的审批流程
    process_code_lst = [(process_code_container, '容器法'), (process_code_circle, '圆管'), (process_code_square, '方渠'),
                        (process_code_machine, '仪器'),
                        (process_code_unable, '无法监测')]

    process_code_dic = {process_code_container: 'fun_container', process_code_circle: 'fun_circle'}
    for i in process_code_dic:
        # print(i)
        getattr(sys.modules[__name__], process_code_dic[i])()


    def fun_container():
        print('容器法')


    def fun_circle():
        print('圆管')


    print(data.get('process_instance').get('title').split('提交')[0])

    # m_s = '12:30'
    # hour_s, min_s = m_s.split(':')
    # monitor_time = datetime.datetime(int(hour_s), int(min_s))
    # print(type(monitor_time), monitor_time)

    t_lst = json.loads(data.get('process_instance').get('form_component_values')[2].get('value'))
    # t_s = t_lst[0]
    # t_s = t_s.split(' ')
    # # print(t_s)
    # year_s, mon_s, day_s = t_s.split(' ')[0].split('-')
    # hour_s, min_s, sec_s = t_s.split(' ')[1].split(':')
    # d_time = datetime.datetime(int(year_s), int(mon_s), int(day_s), int(hour_s), int(min_s), int(sec_s))
    # d_time = datetime.datetime(int(year_s), int(mon_s), int(day_s), int(hour_s), int(min_s))
    # print(type(d_time), d_time)
    # print(type(d_time.time()),d_time.time())
    # print(type(d_time.date()), d_time.date())
    t_data = data.get('process_instance').get('form_component_values')[18].get('value')
    print(type(t_data), t_data)

    # t = {'name': '监测点工作照', 'value': 'null'}
    # print(type(t.get(json.loads(t.get('value')))))
    # print(json.loads(t.get('value')))

    # t2 = {'name': '监测点水流照',
    #       'value': '["https://static.dingtalk.com/media/lADPBE1XX57MSSjNBnTNBDg_1080_1652.jpg","https://static.dingtalk.com/media/lADPBE1XX59Fj0bNBnTNBDg_1080_1652.jpg"]'}
    # print(type(json.loads(t2.get('value'))), json.loads(t2.get('value'))[0])
    # print(os.path.splitext(json.loads(t2.get('value'))[0])[1])
    # for i, j in enumerate(json.loads(t2.get('value'))):
    #     print(i ,j)

    # # t3 = {'name': '监测点', 'value': '测试'}
    # # print(type(json.loads(t3.get('value'))), json.loads(t3.get('value'))[1])
    # print(json.loads('null'))
