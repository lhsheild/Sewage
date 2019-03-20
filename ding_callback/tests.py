import requests


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
    # list = ['https://static.dingtalk.com/media/lADPBE1XX57MOe7NBnTNBDg_1080_1652.jpg', 'https://static.dingtalk.com/media/lADPBE1XX6DgWUHNBnTNBDg_1080_1652.jpg','https://static.dingtalk.com/media/lADPBE1XX59Fj0bNBnTNBDg_1080_1652.jpg', 'https://static.dingtalk.com/media/lADPBE1XX6Dgkw7NBnTNBDg_1080_1652.jpg','https://static.dingtalk.com/media/lADPBE1XX6DgWuLNBnTNBDg_1080_1652.jpg', 'https://static.dingtalk.com/media/lADPBE1XX6Dg2OnNBnTNBDg_1080_1652.jpg']
    # save_img(list)
    data = {'errcode': 0, 'process_instance': {'attached_process_instance_ids': [], 'biz_action': 'NONE',
                                               'business_id': '201903201145000501214',
                                               'cc_userids': ['2504294407695839'], 'create_time': '2019-03-20 11:45:51',
                                               'finish_time': '2019-03-20 11:45:59',
                                               'form_component_values': [{'name': '监测点', 'value': '测试1'},
                                                                         {'name': '监测点物探号', 'value': '测试1'}, {
                                                                             'ext_value': '当前时间:2019-03-20 11:45:49\n当前地点:广西壮族自治区南宁市青秀区南湖街道茶花园路南湖碧园',
                                                                             'name': '["当前时间","当前地点"]',
                                                                             'value': '["2019-03-20 11:45:49",108.363739,22.825241,"广西壮族自治区南宁市青秀区南湖街道茶花园路南湖碧园",47]'},
                                                                         {'name': '监测点外景照',
                                                                          'value': '["https://static.dingtalk.com/media/lADPBE1XX57MOe7NBnTNBDg_1080_1652.jpg","https://static.dingtalk.com/media/lADPBE1XX6DgWUHNBnTNBDg_1080_1652.jpg"]'},
                                                                         {'name': '监测点水流照',
                                                                          'value': '["https://static.dingtalk.com/media/lADPBE1XX59Fj0bNBnTNBDg_1080_1652.jpg","https://static.dingtalk.com/media/lADPBE1XX6Dgkw7NBnTNBDg_1080_1652.jpg"]'},
                                                                         {'name': '监测点工作照',
                                                                          'value': '["https://static.dingtalk.com/media/lADPBE1XX6DgWuLNBnTNBDg_1080_1652.jpg","https://static.dingtalk.com/media/lADPBE1XX6Dg2OnNBnTNBDg_1080_1652.jpg"]'},
                                                                         {'name': '检测时间段', 'value': '12:30'},
                                                                         {'name': '第一次检测时长', 'value': '33'},
                                                                         {'name': '第一次检测水量', 'value': '333'},
                                                                         {'name': '第二次检测时长', 'value': '333'},
                                                                         {'name': '第二次检测水量', 'value': '223'},
                                                                         {'name': '第三次检测时长', 'value': '222'},
                                                                         {'name': '第三次检测水量', 'value': '555'},
                                                                         {'name': '样品编号', 'value': '测试1－1555'},
                                                                         {'name': '检测指标',
                                                                          'value': '["COD NH3-N TP TN","BOD","溶氧量"]'},
                                                                         {'name': '样品照片',
                                                                          'value': '["https://static.dingtalk.com/media/lADPBE1XX57MPFPNBnTNBDg_1080_1652.jpg"]'},
                                                                         {'name': '颜色', 'value': '灰色'},
                                                                         {'name': '气味', 'value': '无味'},
                                                                         {'name': '浑浊度', 'value': '透明'},
                                                                         {'name': '是否合格', 'value': '是'}],
                                               'operation_records': [
                                                   {'date': '2019-03-20 11:45:50', 'operation_result': 'NONE',
                                                    'operation_type': 'START_PROCESS_INSTANCE', 'userid': 'manager405'},
                                                   {'date': '2019-03-20 11:45:58', 'operation_result': 'AGREE',
                                                    'operation_type': 'EXECUTE_TASK_NORMAL', 'remark': '',
                                                    'userid': 'manager405'},
                                                   {'date': '2019-03-20 11:45:58', 'operation_result': 'NONE',
                                                    'operation_type': 'NONE', 'remark': '', 'userid': 'manager405'}],
                                               'originator_dept_id': '104659413', 'originator_dept_name': '水质组',
                                               'originator_userid': 'manager405', 'result': 'agree',
                                               'status': 'COMPLETED', 'tasks': [
            {'create_time': '2019-03-20 11:45:51', 'finish_time': '2019-03-20 11:45:59', 'task_result': 'AGREE',
             'task_status': 'COMPLETED', 'taskid': '60024121247', 'userid': 'manager405'}],
                                               'title': '梁昊提交的流量水质监测（容器法）'}, 'request_id': '6gr853oco6i1'}
