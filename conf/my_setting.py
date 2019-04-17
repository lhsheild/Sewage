import os
from Sewage import settings


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
process_code_lst = [process_code_container, process_code_circle, process_code_square, process_code_machine,
                    process_code_unable]
# 用于回调功能反射的字典
process_code_dic = {process_code_container: 'func_container', process_code_circle: 'func_circle',
                    process_code_square: 'func_square', process_code_machine: 'func_machine',
                    process_code_unable: 'func_unable'}

# 企业ID
corp_id = "ding064ce37e8c6fff8435c2f4657eb6378f"

# 微应用
app_key = 'dingmdy8p4txyehahwqv'
app_secret = 'msKp0WTSjbgcaLmhmBUJhYhqkpWua-Gu8HTvSxhTf1tgIwuf4U50a_CXqoQVzYQg'
"""20190417测试"""
test_app_key = 'dingqzo9n75ruqge7aum'
test_app_secret = '3Sf-Tng0Y4DhPSePmtzM7ZYXxaWiqcJfP34vOrGJXs_tY37p3XCb8hgLHgPK9_mx'

# 加密解密
aes_key = '1234567890123456789012345678901234567890123'
token = '123456'

# 项目路径
# project_path = os.path.dirname(os.getcwd())
project_path = os.getcwd()
# 媒体文件路径
media_path = os.path.join(settings.BASE_DIR, 'media')
# 图片存储路径
img_folder_path = os.path.join(media_path, 'img')
# excel路径
excel_folder = os.path.join(media_path, 'excel')
# 导出路径
export_folder = os.path.join(media_path, 'output')

# 用于导出功能回调的列表
ex_func_lst = ['ex_container', 'ex_circle', 'ex_square', 'ex_machine', 'ex_unable']

if __name__ == '__main__':
    print(settings.BASE_DIR)