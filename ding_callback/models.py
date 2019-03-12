from django.db import models


# Create your models here.
# 容器法
class Monitor_Point(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('监测点号', max_length=64, null=False)
    geophysical_point = models.CharField('物探点号', max_length=64, unique=True.)
    work_function = models.IntegerField('监测方法', max_length=8)
    exterior_photo = models.CharField('外景照', max_length=128)
    water_flow_photo = models.CharField('水流照', max_length=128)
    work_photo = models.CharField('工作照', max_length=128)


class Sample_Info(models.Model):
    id = models.AutoField(primary_key=True)
    monitor_point = models.ForeignKey('监测点号', to='Monitor_Point')


class Sample_Container(models.Model):
    id = models.AutoField(primary_key=True)
    monitor_point = models.ForeignKey('监测点号', to='Monitor_Point')
    sample_date = models.DateTimeField('采样日期', max_length=32)
    sample_time = models.DateTimeField('采样时间段', max_length=32)
    sample_number = models.IntegerField('样品编号',max_length=16, null=False)
    # sample_count = models.IntegerField('样品数量', max_length=8)
    sample_color = models.CharField('样品颜色',max_length=16)
    sample_odor = models.CharField('样品气味',max_length=16)
    sample_turbidity = models.CharField('样品浊度',max_length=16)


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

