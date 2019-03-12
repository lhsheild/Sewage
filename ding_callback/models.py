from django.db import models


# Create your models here.
# 容器法
class Monitor_Point(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('监测点号', max_length=64, null=False)
    geophysical_point = models.CharField('物探点号', max_length=64, unique=True)
    work_function = models.IntegerField('监测方法', max_length=8)
    exterior_photo = models.CharField('外景照', max_length=128)
    water_flow_photo = models.CharField('水流照', max_length=128)
    work_photo = models.CharField('工作照', max_length=128)


class Sample_Info(models.Model):
    id = models.AutoField(primary_key=True)
    sample = models.ForeignKey('样品', to='Sample_Container')
    SS = models.CharField('悬浮物', max_length=16)
    NH3_N = models.CharField('氨氮', max_length=16)
    TP = models.CharField('总磷', max_length=16)
    TN = models.CharField('总氮', max_length=16)
    COD = models.CharField('化学需氧量', max_length=16)
    BOD = models.CharField('五日生化需氧量', max_length=16)
    AIS = models.CharField('阴离子表面活性剂', max_length=16)
    AFVO = models.CharField('动植物油', max_length=16)
    DO = models.CharField('溶解氧', max_length=16)
    FLOW = models.CharField('流量', max_length=16)
    CR = models.CharField('透明度', max_length=16)
    ORP = models.CharField('氧化还原电位', max_length=16)
    SinkableS = models.CharField('易沉固体', max_length=16)
    Sulfide = models.CharField('硫化物', max_length=16)
    Cyanide = models.CharField('氰化物', max_length=16)


class Sample_Container(models.Model):
    id = models.AutoField(primary_key=True)
    monitor_point = models.ForeignKey('监测点号', to='Monitor_Point')
    sample_date = models.DateTimeField('采样日期', max_length=32)
    sample_time = models.DateTimeField('采样时间段', max_length=32)
    sample_number = models.IntegerField('样品编号', max_length=16, null=False)
    # sample_count = models.IntegerField('样品数量', max_length=8)
    sample_color = models.CharField('样品颜色', max_length=16)
    sample_odor = models.CharField('样品气味', max_length=16)
    sample_turbidity = models.CharField('样品浊度', max_length=16)


class Flow_Container(models.Model):
    id = models.AutoField(primary_key=True)
    monitor_point = models.ForeignKey('监测点号', to='Monitor_Point')
    flow_date = models.DateTimeField('流量监测日期', max_length=32)
    flow_time = models.DateTimeField('流量监测时间段', max_length=32)
    time1 = models.IntegerField('监测时长1', max_length=16)
    volume1 = models.IntegerField('监测水量1', max_length=16)
    time2 = models.IntegerField('监测时长2', max_length=16)
    volume2 = models.IntegerField('监测水量2', max_length=16)
    time3 = models.IntegerField('监测时长3', max_length=16)
    volume3 = models.IntegerField('监测水量3', max_length=16)
