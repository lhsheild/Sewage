from django.db import models


# Create your models here.
# 容器法
class MonitorPoint(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('监测点号', max_length=64, null=False)
    geophysical_point = models.CharField('物探点号', max_length=64, unique=True)
    is_monitor = models.IntegerField('是否监测')
    not_monitor_reason = models.CharField('无法监测原因', max_length=128)
    work_function = models.IntegerField('监测方法')  # 0/1/2/3/4 容器/圆管/方渠/仪器/无法监测
    exterior_photo = models.CharField('外景照', max_length=128)
    water_flow_photo = models.CharField('水流照', max_length=128)

    # 仪器法需要的照片
    status_photo = models.CharField('监测点现状照', max_length=128)
    probe_photo = models.CharField('探头照', max_length=128)
    machine_photo = models.CharField('仪器照', max_length=128)
    setup_photo = models.CharField('仪器设置照', max_length=128)

    work_photo = models.CharField('工作照', max_length=128)
    # sample_info = models.ManyToManyField(to='SampleInfo')
    # flow_info = models.ManyToManyField(to='FlowInfo')


class SampleInfo(models.Model):
    id = models.AutoField(primary_key=True)
    monitor_point = models.ForeignKey(to='MonitorPoint', related_name='sample')
    people = models.CharField('采样者', max_length=32)

    sample_date = models.DateField('采样日期', max_length=32)
    sample_time = models.TimeField('采样时间段', max_length=32)
    sample_number = models.CharField('样品编号', max_length=32, null=False)
    # sample_count = models.IntegerField('样品数量', max_length=8)
    sample_color = models.CharField('样品颜色', max_length=32)
    sample_odor = models.CharField('样品气味', max_length=32)
    sample_turbidity = models.CharField('样品浊度', max_length=32)

    SS = models.CharField('悬浮物', max_length=32)
    NH3_N = models.CharField('氨氮', max_length=32)
    TP = models.CharField('总磷', max_length=32)
    TN = models.CharField('总氮', max_length=32)
    COD = models.CharField('化学需氧量', max_length=32)
    BOD = models.CharField('五日生化需氧量', max_length=32)
    AIS = models.CharField('阴离子表面活性剂', max_length=32)
    AFVO = models.CharField('动植物油', max_length=32)
    DO = models.CharField('溶解氧', max_length=32)
    FLOW = models.CharField('流量', max_length=32)
    CR = models.CharField('透明度', max_length=32)
    ORP = models.CharField('氧化还原电位', max_length=32)
    SinkableS = models.CharField('易沉固体', max_length=32)
    Sulfide = models.CharField('硫化物', max_length=32)
    Cyanide = models.CharField('氰化物', max_length=32)


class FlowInfo(models.Model):
    id = models.AutoField(primary_key=True)
    monitor_point = models.ForeignKey(to='MonitorPoint', related_name='flowinfo')
    people = models.CharField('监测者', max_length=32)

    flow_date = models.DateField('流量监测日期', max_length=32)
    flow_time = models.TimeField('流量监测时间段', max_length=32)
    # flow_function = models.IntegerField('监测方法')  # 0/1/2/3/4 容器/圆管/方渠/仪器/无法监测

    # 容器法
    time1 = models.FloatField('监测时长1', max_length=32)
    volume1 = models.FloatField('监测水量1', max_length=32)
    time2 = models.FloatField('监测时长2', max_length=32)
    volume2 = models.FloatField('监测水量2', max_length=32)
    time3 = models.FloatField('监测时长3', max_length=32)
    volume3 = models.FloatField('监测水量3', max_length=32)

    # 圆管
    diameter = models.FloatField('管径', max_length=32)
    mud_depth = models.FloatField('淤泥深度', max_length=32)
    cicle_lequid_level1 = models.FloatField('液位1', max_length=32)
    cicle_instantaneous_flow_rate1 = models.FloatField('瞬时流速1', max_length=32)
    cicle_lequid_level2 = models.FloatField('液位2', max_length=32)
    cicle_instantaneous_flow_rate2 = models.FloatField('瞬时流速2', max_length=32)
    cicle_lequid_level3 = models.FloatField('液位3', max_length=32)
    cicle_instantaneous_flow_rate3 = models.FloatField('瞬时流速3', max_length=32)

    # 方渠
    canal_width = models.FloatField('渠宽', max_length=32)
    square_lequid_level1 = models.FloatField('液位1', max_length=32)
    square_instantaneous_flow_rate1 = models.FloatField('瞬时流速1', max_length=32)
    square_lequid_level2 = models.FloatField('液位2', max_length=32)
    square_instantaneous_flow_rate2 = models.FloatField('瞬时流速2', max_length=32)
    square_lequid_level3 = models.FloatField('液位3', max_length=32)
    square_instantaneous_flow_rate3 = models.FloatField('瞬时流速3', max_length=32)

    # 仪器
    machine_flow = models.FloatField('仪器监测流量', max_length=32)