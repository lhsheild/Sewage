import openpyxl
import os
from statistics import mean
import time
import json
import shutil
import zipfile

from conf import my_setting
from lib.common import list_split
from Sewage import settings


def export


def ex_container(monitor_objs):
    '''
    导出采用容器法的监测点数据
    :param monitor_objs: 监测点对象集
    :return: time_str + '.zip': 压缩包名
    '''
    time_str = time.time()
    time_str = str(time_str)  # 时间戳作为压缩包和临时文件夹名
    output_path = os.path.join(my_setting.export_folder, time_str)
    shutil.rmtree(my_setting.export_folder)
    if not os.path.exists(my_setting.export_folder):
        os.mkdir(my_setting.export_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for monitor_count, monitor in enumerate(monitor_objs):
        monitor_sample_info_dic = {}  # 记录某一监测点的样品信息
        shutil.copy(os.path.join(my_setting.excel_folder, '小区监测统计表.xlsx'), output_path_per_monitor)  # 监测点对应统计表excel表格
        shutil.copy(os.path.join(my_setting.excel_folder, '流量表.xlsx'), output_path_per_monitor)  # 监测点对应流量表excel表格
        output_path_per_monitor = os.path.join(output_path, monitor.name)  # 存放每个监测点相应文件的临时路径
        output_path_for_photo_per_monitor = os.path.join(output_path_per_monitor, '照片')  # 存放每个监测点相应照片的临时路径
        if not os.path.exists(output_path_per_monitor):
            os.mkdir(output_path_per_monitor)
        if not os.path.exists(output_path_for_photo_per_monitor):
            os.mkdir(output_path_for_photo_per_monitor)
        # 外景照
        exterior_photo_lst = json.loads(monitor.exterior_photo)
        exterior_photo_lst = list_split(exterior_photo_lst)
        for exterior_photo in exterior_photo_lst:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, exterior_photo), output_path_for_photo_per_monitor)
        # 水流照
        water_flow_photo_lst = json.loads(monitor.water_flow_photo)
        water_flow_photo_lst = list_split(water_flow_photo_lst)
        for water_photo in water_flow_photo_lst:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, water_photo), output_path_for_photo_per_monitor)
        # 工作照
        work_photo_lst = json.loads(monitor.work_photo)
        work_photo_lst = list_split(work_photo_lst)
        for work_photo in work_photo_lst:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, work_photo), output_path_for_photo_per_monitor)

        # 样品
        samples = monitor.sample.all().order_by('sample_date', 'sample_time')
        static_excel = openpyxl.load_workbook(os.path.join(output_path_per_monitor, '小区监测统计表.xlsx'))
        static_sample = static_excel['水质']
        for sample_count, sample in enumerate(samples):
            # 样品照
            sample_photo_lst = json.loads(sample.sample_photo)
            sample_photo_lst = list_split(sample_photo_lst)
            for sample_photo in sample_photo_lst:
                shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sample_photo), output_path_for_photo_per_monitor)
            # 打开样品统计表
            static_sample['A{}'.format(4 + sample_count)] = sample_count  # 序号
            static_sample['B{}'.format(4 + sample_count)] = monitor.name  # 采样点位
            static_sample['E{}'.format(4 + sample_count)] = monitor.geophysical_point  # 物探点号
            static_sample['H{}'.format(4 + sample_count)] = sample.sample_date  # 采样日期
            static_sample['I{}'.format(4 + sample_count)] = sample.sample_time  # 采样时间段
            static_sample['J{}'.format(4 + sample_count)] = sample.sample_number  # 样品编号
            static_sample[
                'K{}'.format(4 + sample_count)] = sample.sample_color + '、' + sample.sample_odor + '、' + sample.sample_turbidity  # 样品状态
            static_sample['L{}'.format(4 + sample_count)] = sample.monitor_task  # 监测项目
            static_sample['M{}'.format(4 + sample_count)] = sample.sample_count  # 样品数量
            static_sample['N{}'.format(4 + sample_count)] = sample.people  # 采样人
        static_excel.save(os.path.join(output_path_per_monitor, '小区监测统计表.xlsx'))

        #流量
        flows = monitor.flow.all().order_by('flow_date', 'flow_time')


def ex_container_old(monitor_objs):
    time_str = time.time()
    time_str = str(time_str)
    output_path = os.path.join(my_setting.export_folder, time_str)
    shutil.rmtree(my_setting.export_folder)
    if not os.path.exists(my_setting.export_folder):
        os.mkdir(my_setting.export_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    static_excel = os.path.join(output_path, '小区监测统计表.xlsx')
    for count_m, m in enumerate(monitor_objs, 1):  # 遍历所有监测点
        output_path_per_monitor = os.path.join(output_path, m.name)
        output_path_for_photo_per_monitor = os.path.join(output_path_per_monitor, '照片')
        if not os.path.exists(output_path_per_monitor):
            os.mkdir(output_path_per_monitor)
        monitor_flow_dic = {}  # 记录监测点每日流量
        if not os.path.exists(output_path_for_photo_per_monitor):
            os.mkdir(output_path_for_photo_per_monitor)

        exterior_photo = json.loads(m.exterior_photo)
        exterior_photo = list_split(exterior_photo)
        for ep in exterior_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, ep), output_path_for_photo_per_monitor)

        water_flow_photo = json.loads(m.water_flow_photo)
        water_flow_photo = list_split(water_flow_photo)
        for wfp in water_flow_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wfp), output_path_for_photo_per_monitor)

        work_photo = json.loads(m.work_photo)
        work_photo = list_split(work_photo)
        for wp in work_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wp), output_path_for_photo_per_monitor)

        fs = m.flow.all().distinct('flow_date')  # 根据采样时间分组
        f_date_lst = []
        for f in fs:
            f_date_lst.append(f.flow_date)  # 所有的采样日期
        # export_excel_path = os.path.join()
        if count_m == 1:
            m_wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '小区监测统计表.xlsx'))
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']
        else:
            m_wb = openpyxl.load_workbook(static_excel)
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']

        for count_f, i in enumerate(f_date_lst):
            if s_ws['H{}'.format(4 + 3 * count_m - 2)].value != '' and \
                    s_ws['H{}'.format(4 + 3 * count_m - 2)].value is not None and \
                    s_ws['H{}'.format(4 + 3 * count_m - 2)].value != str(i):
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = s_ws['H{}'.format(4 + 3 * count_m - 2)].value + '/' + str(i)
            else:
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = str(i)

            ss = m.sample.filter(sample_date=i).distinct('sample_time').order_by('sample_time')  # 日期’i‘对应的样品表对象
            for s in ss:
                if s.sample_photo != '' and s.sample_photo != 'null' and s.sample_photo is not None:
                    sample_photo = json.loads(s.sample_photo)
                    sample_photo = list_split(sample_photo)
                    for sp in sample_photo:
                        shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sp), output_path_for_photo_per_monitor)
                if str(s.sample_time) == '08:00:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 2)] = '08:00:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 2)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 2)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 2)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 2)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 2)] = s.people
                elif str(s.sample_time) == '12:30:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 1)] = '12:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 1)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 1)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 1)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 1)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 1)] = s.people
                else:
                    s_ws['I{}'.format(4 + 3 * count_m)] = '19:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m)] = s.people
            fs = m.flow.filter(flow_date=i).distinct('flow_time').order_by('flow_time')  # 日期’i‘对应的流量表对象
            wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '流量表.xlsx'))
            ws = wb['流量']
            ws['A4'].value = m.name
            temp_ex_name = m.name + '_' + str(i) + '_' + '流量表.xlsx'
            monitor_flow_excel = os.path.join(output_path_per_monitor, temp_ex_name)
            day_avg_flow_lst = []
            for f in fs:  # 遍历某一采样时间的流量对象
                # print(f.flow_date, f.flow_time,f.volume1)
                if str(f.flow_time) == '08:00:00':
                    time_lst = [f.time1, f.time2, f.time3]
                    flow_lst = [f.volume1, f.volume2, f.volume3]
                    flow1 = (flow_lst[0] / 1000) / time_lst[0]
                    flow2 = (flow_lst[1] / 1000) / time_lst[1]
                    flow3 = (flow_lst[2] / 1000) / time_lst[2]
                    day_avg_flow_lst.append((flow1 + flow2 + flow3) / 3)
                    for j in range(4, 7):
                        temp_time = 'D' + str(j)
                        ws[temp_time].value = time_lst[j - 4]
                        temp_water = 'E' + str(j)
                        ws[temp_water].value = flow_lst[j - 4]
                elif str(f.flow_time) == '12:30:00':
                    time_lst = [f.time1, f.time2, f.time3]
                    flow_lst = [f.volume1, f.volume2, f.volume3]
                    flow1 = (flow_lst[0] / 1000) / time_lst[0]
                    flow2 = (flow_lst[1] / 1000) / time_lst[1]
                    flow3 = (flow_lst[2] / 1000) / time_lst[2]
                    day_avg_flow_lst.append((flow1 + flow2 + flow3) / 3)
                    for j in range(7, 10):
                        temp_time = 'D' + str(j)
                        ws[temp_time].value = time_lst[j - 7]
                        temp_water = 'E' + str(j)
                        ws[temp_water].value = flow_lst[j - 7]
                else:
                    time_lst = [f.time1, f.time2, f.time3]
                    flow_lst = [f.volume1, f.volume2, f.volume3]
                    flow1 = (flow_lst[0] / 1000) / time_lst[0]
                    flow2 = (flow_lst[1] / 1000) / time_lst[1]
                    flow3 = (flow_lst[2] / 1000) / time_lst[2]
                    day_avg_flow_lst.append((flow1 + flow2 + flow3) / 3)
                    for j in range(10, 13):
                        temp_time = 'D' + str(j)
                        ws[temp_time].value = time_lst[j - 10]
                        temp_water = 'E' + str(j)
                        ws[temp_water].value = flow_lst[j - 10]
            intro = '监测日期：{}                观测者：{}                检查者：'.format(i, m.people)
            ws['A2'] = intro
            wb.save(monitor_flow_excel)
            day_avg = mean(day_avg_flow_lst)
            day_total_flow = day_avg * 86400 / 1000
            monitor_flow_dic[str(i)] = day_total_flow
        avg_day_total_flow = mean(monitor_flow_dic.values())
        date_sorted_lst = sorted(monitor_flow_dic.keys())
        start_time = date_sorted_lst[0]
        end_time = date_sorted_lst[-1]
        f_ws['A{}'.format(3 + count_m)] = count_m
        f_ws['B{}'.format(3 + count_m)] = m.name
        f_ws['E{}'.format(3 + count_m)] = m.geophysical_point
        f_ws['L{}'.format(3 + count_m)] = start_time
        f_ws['M{}'.format(3 + count_m)] = end_time
        f_ws['N{}'.format(3 + count_m)] = '当日00:00至24:00'
        f_ws['O{}'.format(3 + count_m)] = avg_day_total_flow
        f_ws['Q{}'.format(3 + count_m)] = '容器法'
        f_ws['R{}'.format(3 + count_m)] = m.people

        s_ws['A{}'.format(4 + 3 * count_m - 2)] = count_m
        s_ws['B{}'.format(4 + 3 * count_m - 2)] = m.name
        s_ws['E{}'.format(4 + 3 * count_m - 2)] = m.geophysical_point
        m_wb.save(static_excel)
    file_news = time_str + '.zip'
    file_news = my_setting.export_folder + os.sep + file_news
    with zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(output_path):
            fpath = dirpath.replace(output_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zf.write(os.path.join(dirpath, filename), fpath + filename)
    shutil.rmtree(output_path)
    return time_str + '.zip'


def ex_circle(monitor_objs):
    time_str = time.time()
    time_str = str(time_str)
    output_path = os.path.join(my_setting.export_folder, time_str)
    shutil.rmtree(my_setting.export_folder)
    if not os.path.exists(my_setting.export_folder):
        os.mkdir(my_setting.export_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    static_excel = os.path.join(output_path, '小区监测统计表.xlsx')
    for count_m, m in enumerate(monitor_objs, 1):  # 遍历所有监测点
        output_path_per_monitor = os.path.join(output_path, m.name)
        output_path_for_photo_per_monitor = os.path.join(output_path_per_monitor, '照片')
        if not os.path.exists(output_path_per_monitor):
            os.mkdir(output_path_per_monitor)
        monitor_flow_dic = {}
        if not os.path.exists(output_path_for_photo_per_monitor):
            os.mkdir(output_path_for_photo_per_monitor)

        exterior_photo = json.loads(m.exterior_photo)
        exterior_photo = list_split(exterior_photo)
        for ep in exterior_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, ep), output_path_for_photo_per_monitor)

        water_flow_photo = json.loads(m.water_flow_photo)
        water_flow_photo = list_split(water_flow_photo)
        for wfp in water_flow_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wfp), output_path_for_photo_per_monitor)

        work_photo = json.loads(m.work_photo)
        work_photo = list_split(work_photo)
        for wp in work_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wp), output_path_for_photo_per_monitor)

        fs = m.flow.all().distinct('flow_date')  # 根据采样时间分组
        f_date_lst = []
        for f in fs:
            f_date_lst.append(f.flow_date)  # 所有的采样日期

        if count_m == 1:
            m_wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '小区监测统计表.xlsx'))
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']
        else:
            m_wb = openpyxl.load_workbook(static_excel)
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']

        for i in f_date_lst:
            if s_ws['H{}'.format(4 + 3 * count_m - 2)].value != '' and s_ws[
                'H{}'.format(4 + 3 * count_m - 2)].value is not None and s_ws[
                'H{}'.format(4 + 3 * count_m - 2)].value != str(i):
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = s_ws['H{}'.format(4 + 3 * count_m - 2)].value + '/' + str(i)
            else:
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = str(i)

            ss = m.sample.filter(sample_date=i).distinct('sample_time').order_by('sample_time')  # 日期’i‘对应的样品表对象
            for s in ss:
                if s.sample_photo != '' and s.sample_photo != 'null' and s.sample_photo is not None:
                    sample_photo = json.loads(s.sample_photo)
                    sample_photo = list_split(sample_photo)
                    for sp in sample_photo:
                        shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sp), output_path_for_photo_per_monitor)
                if str(s.sample_time) == '08:00:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 2)] = '08:00:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 2)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 2)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 2)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 2)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 2)] = s.people
                elif str(s.sample_time) == '12:30:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 1)] = '12:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 1)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 1)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 1)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 1)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 1)] = s.people
                else:
                    s_ws['I{}'.format(4 + 3 * count_m)] = '19:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m)] = s.people

            fs = m.flow.filter(flow_date=i).distinct('flow_time').order_by('flow_time')
            wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '流量表(圆管).xlsx'))
            ws = wb['流量']
            ws['A4'].value = m.name
            temp_ex_name = m.name + '_' + str(i) + '_' + '流量表(圆管).xlsx'
            monitor_flow_excel = os.path.join(output_path_per_monitor, temp_ex_name)
            day_avg_flow_lst = []
            for f in fs:  # 遍历某一采样时间的流量对象
                diameter = f.diameter
                if str(f.flow_time) == '08:00:00':
                    lequid_lst = [f.cicle_lequid_level1, f.cicle_lequid_level2, f.cicle_lequid_level3]
                    instantaneous_lst = [f.cicle_instantaneous_flow_rate1, f.cicle_instantaneous_flow_rate2,
                                         f.cicle_instantaneous_flow_rate3]
                    for j in range(4, 7):
                        temp_dia = 'D' + str(j)
                        ws[temp_dia].value = diameter
                        temp_lequid = 'E' + str(j)
                        ws[temp_lequid].value = lequid_lst[j - 4]
                        temp_instantaneous = 'F' + str(j)
                        ws[temp_instantaneous].value = instantaneous_lst[j - 4]
                elif str(f.flow_time) == '12:30:00':
                    lequid_lst = [f.cicle_lequid_level1, f.cicle_lequid_level2, f.cicle_lequid_level3]
                    instantaneous_lst = [f.cicle_instantaneous_flow_rate1, f.cicle_instantaneous_flow_rate2,
                                         f.cicle_instantaneous_flow_rate3]
                    for j in range(7, 10):
                        temp_dia = 'D' + str(j)
                        ws[temp_dia].value = diameter
                        temp_lequid = 'E' + str(j)
                        ws[temp_lequid].value = lequid_lst[j - 7]
                        temp_instantaneous = 'F' + str(j)
                        ws[temp_instantaneous].value = instantaneous_lst[j - 7]
                else:
                    lequid_lst = [f.cicle_lequid_level1, f.cicle_lequid_level2, f.cicle_lequid_level3]
                    instantaneous_lst = [f.cicle_instantaneous_flow_rate1, f.cicle_instantaneous_flow_rate2,
                                         f.cicle_instantaneous_flow_rate3]
                    for j in range(10, 13):
                        temp_dia = 'D' + str(j)
                        ws[temp_dia].value = diameter
                        temp_lequid = 'E' + str(j)
                        ws[temp_lequid].value = lequid_lst[j - 10]
                        temp_instantaneous = 'F' + str(j)
                        ws[temp_instantaneous].value = instantaneous_lst[j - 10]
            intro = '监测日期：{}                观测者：{}                检查者：'.format(i, m.people)
            ws['A2'] = intro
            wb.save(monitor_flow_excel)
        start_time = str(f_date_lst[0])
        end_time = str(f_date_lst[-1])
        f_ws['A{}'.format(3 + count_m)] = count_m
        f_ws['B{}'.format(3 + count_m)] = m.name
        f_ws['E{}'.format(3 + count_m)] = m.geophysical_point
        f_ws['L{}'.format(3 + count_m)] = start_time
        f_ws['M{}'.format(3 + count_m)] = end_time
        f_ws['N{}'.format(3 + count_m)] = '当日00:00至24:00'
        # f_ws['O{}'.format(3 + count_m)] = avg_day_total_flow
        f_ws['Q{}'.format(3 + count_m)] = '流速法（圆管）'
        f_ws['R{}'.format(3 + count_m)] = m.people

        s_ws['A{}'.format(4 + 3 * count_m - 2)] = count_m
        s_ws['B{}'.format(4 + 3 * count_m - 2)] = m.name
        s_ws['E{}'.format(4 + 3 * count_m - 2)] = m.geophysical_point
        m_wb.save(static_excel)

    file_news = time_str + '.zip'
    file_news = my_setting.export_folder + os.sep + file_news
    with zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(output_path):
            fpath = dirpath.replace(output_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zf.write(os.path.join(dirpath, filename), fpath + filename)
    shutil.rmtree(output_path)
    return time_str + '.zip'


def ex_square(monitor_objs):
    time_str = time.time()
    time_str = str(time_str)
    output_path = os.path.join(my_setting.export_folder, time_str)
    shutil.rmtree(my_setting.export_folder)
    if not os.path.exists(my_setting.export_folder):
        os.mkdir(my_setting.export_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    static_excel = os.path.join(output_path, '小区监测统计表.xlsx')
    for count_m, m in enumerate(monitor_objs, 1):  # 遍历所有监测点
        output_path_per_monitor = os.path.join(output_path, m.name)
        output_path_for_photo_per_monitor = os.path.join(output_path_per_monitor, '照片')
        if not os.path.exists(output_path_per_monitor):
            os.mkdir(output_path_per_monitor)
        monitor_flow_dic = {}
        if not os.path.exists(output_path_for_photo_per_monitor):
            os.mkdir(output_path_for_photo_per_monitor)

        exterior_photo = json.loads(m.exterior_photo)
        exterior_photo = list_split(exterior_photo)
        for ep in exterior_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, ep), output_path_for_photo_per_monitor)

        water_flow_photo = json.loads(m.water_flow_photo)
        water_flow_photo = list_split(water_flow_photo)
        for wfp in water_flow_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wfp), output_path_for_photo_per_monitor)

        work_photo = json.loads(m.work_photo)
        work_photo = list_split(work_photo)
        for wp in work_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wp), output_path_for_photo_per_monitor)

        fs = m.flow.all().distinct('flow_date')  # 根据采样时间分组
        f_date_lst = []
        for f in fs:
            f_date_lst.append(f.flow_date)  # 所有的采样日期
        if count_m == 1:
            m_wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '小区监测统计表.xlsx'))
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']
        else:
            m_wb = openpyxl.load_workbook(static_excel)
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']

        for count_f, i in enumerate(f_date_lst):
            if s_ws['H{}'.format(4 + 3 * count_m - 2)].value != '' and \
                    s_ws['H{}'.format(4 + 3 * count_m - 2)].value is not None and \
                    s_ws['H{}'.format(4 + 3 * count_m - 2)].value != str(i):
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = s_ws['H{}'.format(4 + 3 * count_m - 2)].value + '/' + str(i)
            else:
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = str(i)

            ss = m.sample.filter(sample_date=i).distinct('sample_time').order_by('sample_time')  # 日期’i‘对应的样品表对象
            for s in ss:
                if s.sample_photo != '' and s.sample_photo != 'null' and s.sample_photo is not None:
                    sample_photo = json.loads(s.sample_photo)
                    sample_photo = list_split(sample_photo)
                    for sp in sample_photo:
                        shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sp), output_path_for_photo_per_monitor)
                if str(s.sample_time) == '08:00:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 2)] = '08:00:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 2)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 2)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 2)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 2)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 2)] = s.people
                elif str(s.sample_time) == '12:30:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 1)] = '12:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 1)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 1)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 1)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 1)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 1)] = s.people
                else:
                    s_ws['I{}'.format(4 + 3 * count_m)] = '19:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m)] = s.people

            fs = m.flow.filter(flow_date=i).distinct('flow_time').order_by('flow_time')  # 日期’i‘对应的流量表对象
            wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '流量表(方渠).xlsx'))
            ws = wb['流量']
            ws['A4'].value = m.name
            temp_ex_name = m.name + '_' + str(i) + '_' + '流量表.xlsx'
            monitor_flow_excel = os.path.join(output_path_per_monitor, temp_ex_name)
            day_avg_flow_lst = []
            for f in fs:  # 遍历某一采样时间的流量对象
                canal_width = f.canal_width
                if str(f.flow_time) == '08:00:00':
                    lequid_lst = [f.square_lequid_level1, f.square_lequid_level2, f.square_lequid_level3]
                    instantaneous_lst = [f.square_instantaneous_flow_rate1, f.square_instantaneous_flow_rate2,
                                         f.square_instantaneous_flow_rate3]
                    flow1 = canal_width * lequid_lst[0] * instantaneous_lst[0]
                    flow2 = canal_width * lequid_lst[1] * instantaneous_lst[1]
                    flow3 = canal_width * lequid_lst[2] * instantaneous_lst[2]
                    day_avg_flow_lst.append((flow1 + flow2 + flow3) / 3)
                    for j in range(4, 7):
                        temp_canal = 'D' + str(j)
                        ws[temp_canal].value = canal_width
                        temp_lequid = 'E' + str(j)
                        ws[temp_lequid].value = lequid_lst[j - 4]
                        temp_instantaneous = 'F' + str(j)
                        ws[temp_instantaneous].value = instantaneous_lst[j - 4]
                elif str(f.flow_time) == '12:30:00':
                    lequid_lst = [f.square_lequid_level1, f.square_lequid_level2, f.square_lequid_level3]
                    instantaneous_lst = [f.square_instantaneous_flow_rate1, f.square_instantaneous_flow_rate2,
                                         f.square_instantaneous_flow_rate3]
                    flow1 = canal_width * lequid_lst[0] * instantaneous_lst[0]
                    flow2 = canal_width * lequid_lst[1] * instantaneous_lst[1]
                    flow3 = canal_width * lequid_lst[2] * instantaneous_lst[2]
                    day_avg_flow_lst.append((flow1 + flow2 + flow3) / 3)
                    for j in range(7, 10):
                        temp_canal = 'D' + str(j)
                        ws[temp_canal].value = canal_width
                        temp_lequid = 'E' + str(j)
                        ws[temp_lequid].value = lequid_lst[j - 7]
                        temp_instantaneous = 'F' + str(j)
                        ws[temp_instantaneous].value = instantaneous_lst[j - 7]
                else:
                    lequid_lst = [f.square_lequid_level1, f.square_lequid_level2, f.square_lequid_level3]
                    instantaneous_lst = [f.square_instantaneous_flow_rate1, f.square_instantaneous_flow_rate2,
                                         f.square_instantaneous_flow_rate3]
                    flow1 = canal_width * lequid_lst[0] * instantaneous_lst[0]
                    flow2 = canal_width * lequid_lst[1] * instantaneous_lst[1]
                    flow3 = canal_width * lequid_lst[2] * instantaneous_lst[2]
                    day_avg_flow_lst.append((flow1 + flow2 + flow3) / 3)
                    for j in range(10, 13):
                        temp_canal = 'D' + str(j)
                        ws[temp_canal].value = canal_width
                        temp_lequid = 'E' + str(j)
                        ws[temp_lequid].value = lequid_lst[j - 10]
                        temp_instantaneous = 'F' + str(j)
                        ws[temp_instantaneous].value = instantaneous_lst[j - 13]
            intro = '监测日期：{}                观测者：{}                检查者：'.format(i, m.people)
            ws['A2'] = intro
            wb.save(monitor_flow_excel)
            day_avg = mean(day_avg_flow_lst)
            day_total_flow = day_avg * 86400
            monitor_flow_dic[str(i)] = day_total_flow
        print(monitor_flow_dic)
        avg_day_total_flow = mean(monitor_flow_dic.values())
        print(avg_day_total_flow)
        date_sorted_lst = sorted(monitor_flow_dic.keys())
        start_time = date_sorted_lst[0]
        end_time = date_sorted_lst[-1]
        f_ws['A{}'.format(3 + count_m)] = count_m
        f_ws['B{}'.format(3 + count_m)] = m.name
        f_ws['E{}'.format(3 + count_m)] = m.geophysical_point
        f_ws['L{}'.format(3 + count_m)] = start_time
        f_ws['M{}'.format(3 + count_m)] = end_time
        f_ws['N{}'.format(3 + count_m)] = '当日00:00至24:00'
        f_ws['O{}'.format(3 + count_m)] = avg_day_total_flow
        f_ws['Q{}'.format(3 + count_m)] = '流速法（方渠）'
        f_ws['R{}'.format(3 + count_m)] = m.people

        s_ws['A{}'.format(4 + 3 * count_m - 2)] = count_m
        s_ws['B{}'.format(4 + 3 * count_m - 2)] = m.name
        s_ws['E{}'.format(4 + 3 * count_m - 2)] = m.geophysical_point
        m_wb.save(static_excel)
    file_news = time_str + '.zip'
    file_news = my_setting.export_folder + os.sep + file_news
    with zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(output_path):
            fpath = dirpath.replace(output_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zf.write(os.path.join(dirpath, filename), fpath + filename)
    shutil.rmtree(output_path)
    return time_str + '.zip'


def ex_machine(monitor_objs):
    time_str = time.time()
    time_str = str(time_str)
    output_path = os.path.join(my_setting.export_folder, time_str)
    shutil.rmtree(my_setting.export_folder)
    if not os.path.exists(my_setting.export_folder):
        os.mkdir(my_setting.export_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    static_excel = os.path.join(output_path, '小区监测统计表.xlsx')
    for count_m, m in enumerate(monitor_objs, 1):  # 遍历所有监测点
        output_path_per_monitor = os.path.join(output_path, m.name)
        output_path_for_photo_per_monitor = os.path.join(output_path_per_monitor, '照片')
        if not os.path.exists(output_path_per_monitor):
            os.mkdir(output_path_per_monitor)

        if not os.path.exists(output_path_for_photo_per_monitor):
            os.mkdir(output_path_for_photo_per_monitor)

        status_photo = json.loads(m.status_photo)
        status_photo = list_split(status_photo)
        for sp in status_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sp), output_path_for_photo_per_monitor)

        probe_photo = json.loads(m.probe_photo)
        probe_photo = list_split(probe_photo)
        for pp in probe_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, pp), output_path_for_photo_per_monitor)

        machine_photo = json.loads(m.machine_photo)
        machine_photo = list_split(machine_photo)
        for mp in machine_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, mp), output_path_for_photo_per_monitor)

        setup_photo = json.loads(m.setup_photo)
        setup_photo = list_split(setup_photo)
        for sep in setup_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sep), output_path_for_photo_per_monitor)

        work_photo = json.loads(m.work_photo)
        work_photo = list_split(work_photo)
        for wp in work_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wp), output_path_for_photo_per_monitor)

        ss = m.sample.all().distinct('sample_date')  # 根据采样时间分组
        s_date_lst = []
        for s in ss:
            s_date_lst.append(s.sample_date)  # 所有的采样日期
        if count_m == 1:
            m_wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '小区监测统计表.xlsx'))
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']
        else:
            m_wb = openpyxl.load_workbook(static_excel)
            f_ws = m_wb['流量']
            s_ws = m_wb['水质']

        for count_f, i in enumerate(s_date_lst):
            if s_ws['H{}'.format(4 + 3 * count_m - 2)].value != '' and \
                    s_ws['H{}'.format(4 + 3 * count_m - 2)].value is not None and \
                    s_ws['H{}'.format(4 + 3 * count_m - 2)].value != str(i):
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = s_ws['H{}'.format(4 + 3 * count_m - 2)].value + '/' + str(i)
            else:
                s_ws['H{}'.format(4 + 3 * count_m - 2)] = str(i)

            ss = m.sample.filter(sample_date=i).distinct('sample_time').order_by('sample_time')  # 日期’i‘对应的样品表对象
            for s in ss:
                if s.sample_photo != '' and s.sample_photo != 'null' and s.sample_photo is not None:
                    sample_photo = json.loads(s.sample_photo)
                    sample_photo = list_split(sample_photo)
                    for sp in sample_photo:
                        shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, sp), output_path_for_photo_per_monitor)
                if str(s.sample_time) == '08:00:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 2)] = '08:00:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 2)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 2)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 2)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 2)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 2)] = s.people
                elif str(s.sample_time) == '12:30:00':
                    s_ws['I{}'.format(4 + 3 * count_m - 1)] = '12:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m - 1)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m - 1)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m - 1)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m - 1)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m - 1)] = s.people
                else:
                    s_ws['I{}'.format(4 + 3 * count_m)] = '19:30:00'
                    s_ws['J{}'.format(4 + 3 * count_m)] = s.sample_number
                    s_ws['K{}'.format(
                        4 + 3 * count_m)] = s.sample_color + '、' + s.sample_odor + '、' + s.sample_turbidity
                    s_ws['L{}'.format(4 + 3 * count_m)] = s.monitor_task
                    s_ws['M{}'.format(4 + 3 * count_m)] = s.sample_count
                    s_ws['N{}'.format(4 + 3 * count_m)] = s.people

        s_ws['A{}'.format(4 + 3 * count_m - 2)] = count_m
        s_ws['B{}'.format(4 + 3 * count_m - 2)] = m.name
        s_ws['E{}'.format(4 + 3 * count_m - 2)] = m.geophysical_point
        m_wb.save(static_excel)

    file_news = time_str + '.zip'
    file_news = my_setting.export_folder + os.sep + file_news
    with zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(output_path):
            fpath = dirpath.replace(output_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zf.write(os.path.join(dirpath, filename), fpath + filename)
    shutil.rmtree(output_path)
    return time_str + '.zip'


def ex_unable(monitor_objs):
    time_str = time.time()
    time_str = str(time_str)
    output_path = os.path.join(my_setting.export_folder, time_str)
    shutil.rmtree(my_setting.export_folder)
    if not os.path.exists(my_setting.export_folder):
        os.mkdir(my_setting.export_folder)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    static_excel = os.path.join(output_path, '小区监测统计表.xlsx')
    for count_m, m in enumerate(monitor_objs, 1):  # 遍历所有监测点
        output_path_per_monitor = os.path.join(output_path, m.name)
        record_txt = os.path.join(output_path_per_monitor, '无法监测原因.txt')
        if not os.path.exists(output_path_per_monitor):
            os.mkdir(output_path_per_monitor)

        exterior_photo = json.loads(m.exterior_photo)
        exterior_photo = list_split(exterior_photo)
        for ep in exterior_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, ep), output_path_per_monitor)

        water_flow_photo = json.loads(m.water_flow_photo)
        water_flow_photo = list_split(water_flow_photo)
        for wfp in water_flow_photo:
            shutil.copy('{}{}{}'.format(settings.BASE_DIR, os.sep, wfp), output_path_per_monitor)

        if count_m == 1:
            m_wb = openpyxl.load_workbook(os.path.join(my_setting.excel_folder, '小区监测统计表.xlsx'))
            f_ws = m_wb['流量']
        else:
            m_wb = openpyxl.load_workbook(static_excel)
            f_ws = m_wb['流量']
        f_ws['A{}'.format(3 + count_m)] = count_m
        f_ws['B{}'.format(3 + count_m)] = m.name
        f_ws['E{}'.format(3 + count_m)] = m.geophysical_point
        f_ws['L{}'.format(3 + count_m)] = m.start_time
        f_ws['M{}'.format(3 + count_m)] = m.start_time
        f_ws['N{}'.format(3 + count_m)] = '当日00:00至24:00'
        f_ws['P{}'.format(3 + count_m)] = m.not_monitor_reason
        f_ws['Q{}'.format(3 + count_m)] = '无法监测'
        f_ws['R{}'.format(3 + count_m)] = m.people
        m_wb.save(static_excel)
        reason = m.not_monitor_reason
        with open(record_txt, 'w') as f:
            f.write(reason)
    file_news = time_str + '.zip'
    file_news = my_setting.export_folder + os.sep + file_news
    with zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(output_path):
            fpath = dirpath.replace(output_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                zf.write(os.path.join(dirpath, filename), fpath + filename)
    shutil.rmtree(output_path)
    return time_str + '.zip'
