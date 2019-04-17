import os

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
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sewage.settings")
    import django

    django.setup()

    # d1 = {'event_time': 1553995508000, 'call_back_tag': 'bpms_instance_change',
    #       'bpms_instance_change': {'corpid': 'ding064ce37e8c6fff8435c2f4657eb6378f',
    #                                'bpmsCallBackData': {'createTime': 1553956752000, 'title': '梁昊提交的流量水质监测（容器法）',
    #                                                     'staffId': 'manager405',
    #                                                     'processCode': 'PROC-ELYJ1A4W-7WJ39FFR3417CDU1EEOZ2-D8YFWXSJ-2',
    #                                                     'processInstanceId': '6996855b-d590-4ac7-b132-52d74d96c6e0',
    #                                                     'bizCategoryId': '', 'EventType': 'bpms_instance_change',
    #                                                     'type': 'delete',
    #                                                     'corpId': 'ding064ce37e8c6fff8435c2f4657eb6378f'}}}
    #
    # failed_list = {'event_time': 1553959282000, 'call_back_tag': 'bpms_instance_change',
    #       'bpms_instance_change': {'corpid': 'ding064ce37e8c6fff8435c2f4657eb6378f',
    #                                'bpmsCallBackData': {'result': 'agree', 'createTime': 1553958191000,
    #                                                     'title': '梁昊提交的流量水质监测（容器法）', 'staffId': 'manager405',
    #                                                     'processCode': 'PROC-ELYJ1A4W-7WJ39FFR3417CDU1EEOZ2-D8YFWXSJ-2',
    #                                                     'processInstanceId': '351783dd-182b-471a-8fd6-540011973b8c',
    #                                                     'bizCategoryId': '', 'finishTime': 1553959283000,
    #                                                     'EventType': 'bpms_instance_change', 'type': 'finish',
    #                                                     'url': 'https://aflow.dingtalk.com/dingtalk/mobile/homepage.htm?corpid=ding064ce37e8c6fff8435c2f4657eb6378f&dd_share=false&showmenu=true&dd_progress=false&back=native&procInstId=351783dd-182b-471a-8fd6-540011973b8c&taskId=&swfrom=isv&dinghash=approval&dd_from=#approval',
    #                                                     'corpId': 'ding064ce37e8c6fff8435c2f4657eb6378f'}}}
    import datetime
    monitor_time = datetime.datetime(int(2018), int(9), int(10), int(8), int(0)).time()
    print(str(monitor_time), type(str(monitor_time)))
    name = 'T-1'
    print(name+'-1')
