import requests
import os
import json
import datetime
import itertools
import openpyxl
from statistics import mean

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

    ms = models.MonitorPoint.objects.filter(people='曾玄介', work_function=0)
    for m in ms:
        ss = m.sample.all().order_by('sample_date', 'sample_time')

        for s in ss:
            print(m.name, '**',s.sample_date, '**', s.sample_time)